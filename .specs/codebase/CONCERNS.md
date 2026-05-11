# Codebase Concerns

**Analysis Date:** 2026-05-11

## Tech Debt

### Monolithic `views.py`

- Issue: All 20+ views in a single `estoque/views.py` file (533 lines) — no separation by domain or entity
- Files: `estoque/views.py`
- Why: Single Django app pattern, grew organically
- Impact: Hard to navigate, merge conflicts, testing difficulty
- Fix approach: Split into `views/` package with modules per entity (produtos.py, pedidos.py, entradas.py, etc.)

### Flat tests.py

- Issue: All tests in a single `estoque/tests.py` file
- Files: `estoque/tests.py`
- Why: Django default
- Impact: Will become unmanageable as coverage grows
- Fix approach: Convert to `tests/` package with modules per domain

### No type hints

- Issue: Entire codebase has zero type annotations
- Files: All `.py` files
- Why: Not established as convention
- Impact: No static analysis, harder to refactor, IDE autocomplete degraded
- Fix approach: Gradual adoption on new code, mypy in CI

### Duplicate form init logic

- Issue: `EntradaForm.__init__` and `PedidoForm.__init__` both repeat the same pattern for dynamic setor queryset filtering by unidade
- Files: `estoque/forms.py:78-92`, `forms.py:119-133`
- Why: Copy-paste
- Impact: Bug fix for one won't apply to the other
- Fix approach: Extract into a mixin or shared helper

## Known Bugs

### Stock reservation race condition

- Symptoms: Two concurrent requests reserving stock for the same product could oversell
- Trigger: Rapid double-click on "Reservar" button, or simultaneous requests
- Files: `estoque/signals.py:20-32`
- Workaround: None
- Root cause: No pessimistic locking (`select_for_update()`) around stock reservation logic
- Fix approach: Use `select_for_update()` on Produto rows inside the signal, or wrap in `transaction.atomic()`

### No stock release on status change from EMPENHADO to CANCELADO

- Symptoms: If a pedido is EMPENHADO (empenho uploaded) and then cancelled, the reservation is released, but the empenho file remains uploaded — no cleanup
- Files: `estoque/signals.py:51-58`
- Root cause: Signal only handles RESERVADO/EMPENHADO → CANCELADO but doesn't clean empenho_anexo file
- Fix approach: Clear `empenho_anexo` field when cancelling an EMPENHADO pedido

### Entrada doesn't track user/operator

- Symptoms: Stock entries have no record of who created them
- Files: `estoque/models.py:158-199`
- Impact: No audit trail for inventory additions
- Fix approach: Add `criado_por` ForeignKey to User

## Security Considerations

### No permission checks beyond authentication

- Risk: All views require `@login_required` but no role-based permissions — any authenticated user can create/delete anything
- Files: `estoque/views.py` (all views)
- Current mitigation: None
- Recommendations: Implement Django Groups/Permissions, assign roles (Almoxarife, Comprador, Secretaria, Admin)

### CSRF_TRUSTED_ORIGINS wildcard

- Risk: ALLOWED_HOSTS accepts `*` by default, which auto-populates CSRF_TRUSTED_ORIGINS
- Files: `core/settings.py:34-50`
- Current mitigation: This only applies to DEBUG deployments
- Recommendations: Restrict ALLOWED_HOSTS in production explicitly

## Performance Bottlenecks

### N+1 in pedido_detail stock calculation

- Problem: `pedido_detail` iterates `pedido.itens.all()` and accesses `item.total_pedido`, `item.total_atendido` etc. in a loop, triggering repeated queries for each item
- Files: `estoque/views.py:339-355`
- Measurement: 1 + N queries where N = number of items
- Improvement path: Already has `select_related("produto", "produto__categoria")` which mitigates the main N+1; remaining property calls are in-memory

## Fragile Areas

### Stock mutation via pre_save signal

- Files: `estoque/signals.py:20-58`
- Why fragile: Pre-save signals run on every save; comparing old/new status via a separate DB query (`Pedido.objects.get(pk=instance.pk)`) has race conditions; no transaction wrapping
- Common failures: Race conditions on concurrent save, silent failures if signal raises
- Safe modification: Always test with concurrent scenarios; wrap critical paths in `transaction.atomic()` + `select_for_update()`
- Test coverage: Not tested

### InlineFormSet stock entry

- Files: `estoque/views.py:282-296`
- Why fragile: Post-save signal on ItemEntrada updates stock. If formset has multiple items, each triggers an individual signal. If one item fails mid-way, partial stock updates have already occurred
- Safe modification: Wrap the entire entrada_create flow in `transaction.atomic()`
- Test coverage: Not tested

## Test Coverage Gaps

### Critical stock flows

- What's not tested: Stock entry signals (`atualizar_estoque_entrada`), Pedido lifecycle (`gerenciar_fluxo_estoque`), insufficient stock validation, cancel flow
- Risk: Silent data corruption if stock logic has bugs
- Priority: High
- Difficulty to test: Medium — signals are well-isolated and testable

### CRUD views

- What's not tested: All create/update/delete views and their redirect/error behavior
- Risk: Broken forms, wrong redirects, permission bypass
- Priority: Medium

### Forms validation

- What's not tested: Form validation rules, dynamic queryset filtering
- Priority: Low
