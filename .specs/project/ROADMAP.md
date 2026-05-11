# Roadmap

**Current Milestone:** Core Inventory Management
**Status:** In Progress

---

## Milestone 1: Core Inventory Management

**Goal:** Full inventory cycle — cadastro, entrada, saída com fluxo de empenho, relatórios básicos
**Target:** Shipped (v1 features complete in codebase)

### Features

**Autenticação e Perfis** — COMPLETE

- Login/logout via Django auth
- Perfil de usuário com tema de interface

**Cadastros Base** — COMPLETE

- CRUD de Produtos (categoria, unidade, estoque mínimo)
- CRUD de Fornecedores (CNPJ, contato)
- CRUD de Unidades/Secretarias e Setores
- Vínculo de produtos a fornecedores

**Entrada de Estoque** — COMPLETE

- Entrada com nota fiscal, licitação, lote
- Itens com quantidade e preço unitário
- Atualização automática de estoque via signal
- Suporte a compra direta e licitação

**Saída (Pedidos)** — COMPLETE

- Criação de pedido com itens
- Fluxo: Solicitado → Reservado → Empenhado → Entregue → Cancelado
- Reserva de estoque com validação de saldo
- Anexação de empenho PDF
- Baixa efetiva do estoque

**Relatórios** — PLANNED (improvement requested)

- Relatório de Movimento (consumo por secretaria, entradas por categoria)
- Relatório de Estoque (estoque atual, crítico, valores)
- Relatório de Pedidos (status totals, itens solicitados/atendidos)
- *User indicated this as the next area of work*

**UI / Tema** — COMPLETE

- Dual theme system (classic ERP / modern)
- Design tokens via CSS custom properties
- Keyboard shortcuts (F2-F8, Esc)

---

## Milestone 2: Data Integrity & Hardening

**Goal:** Eliminate race conditions, add audit trails, lock down permissions
**Target:** Not started

### Features

**Stock Integrity** — PLANNED

- `select_for_update()` on stock reservation
- Transaction atomic wrapping on entrada + pedido flows
- Clear empenho file on cancel

**Permissions & Audit** — PLANNED

- Role-based permissions (Almoxarife, Comprador, Secretaria, Admin)
- User tracking on stock entries
- Complete audit log

**Test Coverage Phase 1** — PLANNED

- Signal tests for stock mutation
- CRUD view tests
- Form validation tests

---

## Milestone 3: Reporting & Productivity

**Goal:** Advanced reports, data export, import workflows
**Target:** Not started

### Features

**Advanced Reports** — PLANNED

- Export to CSV/XLSX
- Filter presets and date ranges
- Scheduled report generation

**Bulk Operations** — PLANNED

- Real importação de licitação via planilha
- Bulk product import
- Batch pedido processing

---

## Future Considerations

- API REST para integração com sistema contábil (SIG)
- Notificações por email quando estoque crítico
- Dashboard gráfico com Chart.js ou similar
- App mobile para conferência de estoque
- Multi-exercício (separação de estoque por ano fiscal)
