# Analytics & Produtividade Tasks

**Design:** `.specs/features/analytics-produtividade/design.md`
**Status:** Done

---

## Execution Plan

### Phase 1: Dashboard Charts (Sequential)

```
T1 ──→ T2
```

### Phase 2: Batch Operations (Sequential)

```
T2 ──→ T3 ──→ T4
```

### Phase 3: Verification (Sequential)

```
T4 ──→ T5
```

---

## Task Breakdown

### T1: Add Chart.js CDN to base.html

**What:** Adicionar `<script>` tag do Chart.js 4.4.7 CDN ao `<head>` de `base.html`
**Where:** `templates/base.html`
**Depends on:** None
**Reuses:** Existing CDN pattern (Tailwind via `cdn.tailwindcss.com`, Alpine.js via `unpkg.com`)
**Requirement:** DASH-04

**Done when:**
- [ ] `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js" defer></script>` adicionado antes de `</head>`
- [ ] Posicionado após Alpine.js, antes do bloco `<style>`

**Tests:** none (infraestrutura de script — validado visualmente)
**Gate:** none

---

### T2: Enhance Dashboard with Charts, KPI Variance, and Critical Stock Banner

**What:** Atualizar `dashboard.py` para computar dados de gráficos (JSON) + KPIs com variação mensal. Atualizar `dashboard.html` para renderizar gráficos Chart.js, KPIs aprimorados e banner de estoque crítico.
**Where:**
- `estoque/views/dashboard.py` (modify)
- `templates/estoque/dashboard.html` (modify)
**Depends on:** T1
**Reuses:** `_base.py` model imports, `render`, `TruncMonth`, `date`, `timedelta`
**Requirement:** DASH-01, DASH-02, DASH-03, DASH-05, ALERT-01, ALERT-02, ALERT-03

**Done when:**
- [ ] `_chart_consumo_secretaria()` retorna `{labels: [...], datasets: [{label, data}, ...]}` para últimos 6 meses
- [ ] `_chart_consumo_categoria()` retorna `{labels: [...], data: [...]}` agregado por categoria
- [ ] `_kpi_variance()` retorna 3 indicadores com `{label, current, previous, direction, percent}`
- [ ] Template renderiza `<canvas>` para gráfico de barras com dados do `chart_consumo_json`
- [ ] Template renderiza `<canvas>` para gráfico de pizza com dados do `chart_categoria_json`
- [ ] Template exibe KPIs com seta ↑/↓ e percentual de variação
- [ ] Banner de estoque crítico com link para `relatorio_estoque?apenas_criticos=1`
- [ ] Banner verde "Estoque regular" quando sem itens críticos
- [ ] Estado vazio para gráficos sem dados (mensagem "Sem dados no período")
- [ ] Gate check passes: `uv run python manage.py test estoque.tests.test_views_dashboard -v 2`
- [ ] Test count: >= 3 tests pass (dashboard render, critical banner, empty state)

**Tests:** integration
**Gate:** full

---

### T3: Create Batch Product Import

**What:** Criar view `importar_produtos` com upload de planilha XLSX, preview e confirmação. Criar template dedicado. Registrar URL e view no `__init__.py`.
**Where:**
- `estoque/views/importar_produtos.py` (create)
- `templates/estoque/importar_produtos.html` (create)
- `estoque/views/__init__.py` (modify — add export)
- `estoque/urls.py` (modify — add route)
**Depends on:** T2 (sequencial para evitar conflito em urls.py)
**Reuses:** `_tem_papel` decorator, `importar_licitacao` session-storage pattern, `openpyxl`, `transaction.atomic()`, `messages`
**Requirement:** BATCH-01, BATCH-02, BATCH-04

**Done when:**
- [ ] GET → renderiza form de upload com `action-btn`
- [ ] POST com arquivo → processa XLSX (colunas: Nome, Categoria, Unidade, Estoque Mínimo), salva preview na session
- [ ] Preview exibe tabela com produtos a importar (nome, categoria, unidade, estoque_minimo)
- [ ] Produtos já existentes (match por nome) marcados como "Já cadastrado" no preview
- [ ] POST com `confirmar=1` → cria produtos via `get_or_create`, message de sucesso com contagem
- [ ] Categoria nova é criada automaticamente via `get_or_create`
- [ ] Linhas inválidas (nome vazio) são ignoradas com aviso
- [ ] Unidade inválida default para "UN"
- [ ] Estoque mínimo não numérico default para 0
- [ ] Restrito a "Almoxarife", "Comprador", "Administrador" via `_tem_papel`
- [ ] Link "Importar Produtos" adicionado ao sidebar em "Cadastros"
- [ ] Gate check passes: `uv run python manage.py test estoque.tests.test_views_importar_produtos -v 2`
- [ ] Test count: >= 3 tests pass (upload preview, confirm import, permission deny)

**Tests:** integration
**Gate:** full

---

### T4: Add Batch Stock Minimum Update

**What:** Adicionar endpoint `produto_lote_estoque` para atualizar `estoque_minimo` de múltiplos produtos. Adicionar modal com checkbox de seleção na listagem de produtos.
**Where:**
- `estoque/views/produtos.py` (modify — add view)
- `templates/estoque/produto_list.html` (modify — add checkbox col + modal + button)
- `estoque/views/__init__.py` (modify — add export)
- `estoque/urls.py` (modify — add route)
**Depends on:** T3 (sequencial para evitar conflito em urls.py)
**Reuses:** `_tem_papel` decorator, Alpine.js modal pattern (já existente no template), `bulk_update`
**Requirement:** BATCH-03

**Done when:**
- [ ] Checkbox por produto na listagem com "Selecionar todos" no header
- [ ] Botão "Lote → Estoque Mín" na sidebar de ações
- [ ] Modal com campo `estoque_minimo` (Decimal) e botão "Aplicar a Selecionados"
- [ ] POST atualiza `estoque_minimo` dos produtos selecionados via `QuerySet.update()`
- [ ] Mensagem de sucesso: "Estoque mínimo atualizado para N produto(s)"
- [ ] Sem produtos selecionados → `messages.warning`
- [ ] Restrito a "Almoxarife", "Comprador", "Administrador" via `_tem_papel`
- [ ] Gate check passes: `uv run python manage.py test estoque.tests.test_views_produto -v 2`
- [ ] Test count: >= 2 tests pass (batch update success, no selection warning)

**Tests:** integration
**Gate:** full

---

### T5: Full Verification and Docs Update

**What:** Executar suite completa de testes, verificar que todos passam, atualizar STATE.md e ROADMAP.md com progresso.
**Where:**
- `.specs/project/STATE.md` (modify)
- `.specs/project/ROADMAP.md` (modify if needed)
**Depends on:** T4
**Reuses:** N/A

**Done when:**
- [ ] `uv run python manage.py test -v 2` — todos os testes passam (zero failures)
- [ ] `uv run python manage.py check --deploy` — zero warnings
- [ ] STATE.md atualizado com tarefas concluídas
- [ ] ROADMAP.md M5 marcado com features concluídas

**Tests:** none
**Gate:** build

---

## Parallel Execution Map

```
Phase 1 (Sequential):
  T1 ──→ T2

Phase 2 (Sequential):
  T2 ──→ T3 ──→ T4

Phase 3:
  T4 ──→ T5
```

---

## Task Granularity Check

| Task | Scope | Status |
| --- | --- | --- |
| T1: Add Chart.js CDN | 1 file, 1 script tag | ✅ Granular |
| T2: Enhance dashboard | 2 files (view + template), cohesive feature | ✅ OK |
| T3: Create batch product import | 4 files (view, template, init, urls), single feature | ⚠️ Cohesive but 4 files |
| T4: Add batch stock min update | 4 files (view, template, init, urls), single feature | ⚠️ Cohesive but 4 files |
| T5: Full verification | Docs update only | ✅ Granular |

---

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | None (start) | ✅ Match |
| T2 | T1 | T1 → T2 | ✅ Match |
| T3 | T2 | T2 → T3 | ✅ Match |
| T4 | T3 | T3 → T4 | ✅ Match |
| T5 | T4 | T4 → T5 | ✅ Match |

---

## Test Co-location Validation

| Task | Code Layer | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1: Add CDN | Template (infra, no logic) | integration | none | ✅ OK (infra only) |
| T2: Dashboard enhancement | Views + Templates | integration | integration | ✅ OK |
| T3: Batch product import | Views + Templates | integration | integration | ✅ OK |
| T4: Batch stock min update | Views + Templates | integration | integration | ✅ OK |
| T5: Verification | None (docs) | none | none | ✅ OK |
