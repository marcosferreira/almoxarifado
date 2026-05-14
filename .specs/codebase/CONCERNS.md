# Codebase Concerns

**Analysis Date:** 2026-05-11
**Last Updated:** 2026-05-14

## Tech Debt

### ~~Monolithic `views.py`~~ ✅ Resolvido
- Resolvido em: `ee7ebf1 refactor(views): modularizar views do app estoque`

### ~~Flat tests.py~~ ✅ Resolvido
- Resolvido em: branch `dev` (2026-05-14)
- Convertido para pacote `tests/` com módulos: `test_base`, `test_perfil`, `test_signals`, `test_views_produto`, `test_views_relatorio`, `test_views_importar`

### ~~No type hints~~ ✅ Resolvido
- Resolvido em: branch `dev` (2026-05-14)
- Adicionados type hints em todos os arquivos `.py` do projeto

### ~~Duplicate form init logic~~ ✅ Resolvido
- Resolvido em: branch `dev` (2026-05-14)
- Extraído para `_DynamicSetorFilterMixin` em `forms.py`, usado por `EntradaForm` e `PedidoForm`

## Known Bugs

### ~~Stock reservation race condition~~ ✅ Resolvido
- Resolvido em: `59dd548 feat(estoque): adicionar grupos de permissao e lock transacional`
- Corrigido com `select_for_update()` + `transaction.atomic()`

### ~~No stock release on status change from EMPENHADO to CANCELADO~~ ✅ Resolvido
- Resolvido em: branch `dev` (2026-05-14)
- Adicionada limpeza de `empenho_anexo` no signal `gerenciar_fluxo_estoque` ao cancelar de EMPENHADO

### ~~Entrada doesn't track user/operator~~ ✅ Resolvido
- Resolvido em: branch `dev` (2026-05-14)
- Adicionado campo `criado_por` (FK User) ao modelo `Entrada`
- `entrada_create` e `importar_licitacao` populam o campo automaticamente

## Security Considerations

### ~~No permission checks beyond authentication~~ ✅ Resolvido
- Resolvido em: `59dd548 feat(estoque): adicionar grupos de permissao e lock transacional`
- Implementado decorator `_tem_papel` com grupos: Almoxarife, Comprador, Solicitante, Administrador

### CSRF_TRUSTED_ORIGINS wildcard
- Risk: ALLOWED_HOSTS accepts `*` by default, which auto-populates CSRF_TRUSTED_ORIGINS
- Files: `core/settings.py:34-50`
- Current mitigation: This only applies to DEBUG deployments
- Recommendations: Restrict ALLOWED_HOSTS in production explicitly

## Performance Bottlenecks

### N+1 in pedido_detail stock calculation
- Problem: `pedido_detail` iterates `pedido.itens.all()` and accesses `item.total_pedido`, `item.total_atendido` etc. in a loop, triggering repeated queries for each item
- Files: `estoque/views/pedidos.py:50-60`
- Measurement: 1 + N queries where N = number of items
- Improvement path: Already has `select_related("produto", "produto__categoria")` which mitigates the main N+1; remaining property calls are in-memory

## Fragile Areas

### Stock mutation via pre_save signal
- Files: `estoque/signals.py`
- Mitigated: Uses `select_for_update()` + `transaction.atomic()` on all critical paths. Empenho cleanup added for cancel flow.
- Test coverage: Covered by `EstoqueSignalTests` (4 tests)

### ~~InlineFormSet stock entry~~ ✅ Resolvido
- Resolvido em: branch `dev` (2026-05-14)
- `entrada_create` e `entrada_delete` envolvidos em `transaction.atomic()`
- Test coverage: Covered by `ImportarLicitacaoViewTests` (importação usa `transaction.atomic`)

## Test Coverage Gaps

### ~~Critical stock flows~~ ✅ Resolvido
- Covered by `EstoqueSignalTests` (4 tests: reserva, entrega, cancelamento, estoque insuficiente)

### CRUD views
- What's not tested: All create/update/delete views and their redirect/error behavior
- Risk: Broken forms, wrong redirects, permission bypass
- Priority: Medium

### Forms validation
- What's not tested: Form validation rules, dynamic queryset filtering
- Priority: Low
