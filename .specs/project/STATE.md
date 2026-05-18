# State

**Last Updated:** 2026-05-15T00:00:00-03:00
**Current Work:** Milestone 5 — Dashboard Analytics & Batch Operations implemented

---

## Recent Decisions

### AD-001: Single .specs directory in project root (2026-05-11)

**Decision:** Place `.specs/` at project root (`/smaf/almoxarifado/.specs/`)
**Reason:** Keeps project context alongside source code, version-controlled, accessible to all tools
**Trade-off:** Adds top-level directory but stays hidden (dotfile)
**Impact:** All planning artifacts share the same repo as code

### AD-002: Brownfield mapping before feature work (2026-05-11)

**Decision:** Document existing codebase in 7 brownfield files before any feature work
**Reason:** This is an existing project with zero specs — must understand current state before adding features
**Trade-off:** Upfront documentation cost before visible feature delivery
**Impact:** Future features will reference these docs for decisions

---

## Active Blockers

None

---

## Lessons Learned

None

---

## Quick Tasks Completed

| # | Description | Date | Commit | Status |
|---|---|---|---|---|
| 001 | Initial brownfield mapping (7 files) + PROJECT.md + ROADMAP.md + STATE.md | 2026-05-11 | - | ✅ Done |

---

## Deferred Ideas

- None

---

## Todos

- [x] Relatórios básicos — já implementados (3 views: movimento, estoque, pedidos)
- [x] Fechar lacunas de CRUD: exclusão de Produto, edição/exclusão de Fornecedor e Entrada (Milestone 2)
- [x] Corrigir race condition de reserva de estoque com `select_for_update()` (Milestone 2)
- [x] Implementar permissões por papel (Almoxarife, Comprador, Solicitante, Admin) (Milestone 2)
- [x] Geração de PDF para guia de saída e ficha de produto (Milestone 3)
- [x] Relatórios avançados com filtros por data, exportação CSV/XLSX (Milestone 3)
- [x] Implementar importação real de licitação via planilha (substituir placeholder) (Milestone 3)
- [x] Adicionar testes de signals, views e formulários — 19 testes (Milestone 4)
- [x] Dividir views.py em pacote views/ por entidade (Milestone 4)
- [x] Dashboard com gráficos Chart.js (consumo por secretaria, por categoria) + KPIs com variação mensal (Milestone 5)
- [x] Banner de alerta de estoque crítico no dashboard (Milestone 5)
- [x] Importação em lote de produtos via planilha XLSX (Milestone 5)
- [x] Atualização em lote de estoque mínimo via listagem de produtos (Milestone 5)
- [x] Testes para dashboard, importação de produtos e lote de estoque mínimo — 15 testes (Milestone 5)

---

## Preferences

**Model Guidance Shown:** never
