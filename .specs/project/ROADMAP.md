# Roadmap

**Current Milestone:** CRUD Completion & Data Integrity
**Status:** In Progress

---

## Milestone 1: Core Inventory Management

**Goal:** Full inventory cycle — cadastro, entrada, saída com fluxo de empenho, relatórios básicos
**Target:** Shipped

### Features

**Autenticação e Perfis** — COMPLETE

- Login/logout via Django auth
- Perfil de usuário com seleção de tema de interface
- Troca de senha pelo perfil

**Cadastros Base** — IN PROGRESS

- CRUD completo de Unidades/Secretarias e Setores ✓
- Criação e listagem de Produtos (categoria, unidade, estoque mínimo) ✓
- Edição de Produto ✓
- Criação e listagem de Fornecedores (CNPJ, contato) ✓
- Vínculo de produtos a fornecedores ✓
- ⚠ Faltam: exclusão de Produto, edição/exclusão de Fornecedor

**Entrada de Estoque** — IN PROGRESS

- Entrada com nota fiscal, licitação, lote, programa, empenho ✓
- Itens com quantidade e preço unitário ✓
- Atualização automática de estoque via signal ✓
- Suporte a compra direta e licitação ✓
- ⚠ Faltam: edição e exclusão de Entrada

**Saída (Pedidos)** — COMPLETE

- Criação de pedido com múltiplos itens
- Fluxo: Solicitado → Reservado → Empenhado → Entregue → Cancelado
- Reserva de estoque com validação de saldo disponível
- Anexação de empenho PDF como gate obrigatório
- Baixa efetiva do estoque na confirmação de entrega
- Cancelamento com liberação automática de reserva

**Relatórios Básicos** — COMPLETE

- Relatório de Movimento (consumo por secretaria, entradas por categoria)
- Relatório de Estoque (atual, crítico, disponível, mínimo)
- Relatório de Pedidos (resumo por status, totais solicitado/atendido)

**UI / Tema** — COMPLETE

- Dual theme system (classic ERP / modern)
- Design tokens via CSS custom properties
- Keyboard shortcuts (F2-F8, Esc)

---

## Milestone 2: CRUD Completion & Data Integrity

**Goal:** Fechar lacunas de CRUD, eliminar race conditions e garantir integridade do estoque
**Target:** Próximo

### Features

**CRUD Completo** — PLANNED

- Exclusão de Produto (com proteção se houver movimentações)
- Edição e exclusão de Fornecedor
- Edição e exclusão de Entrada de Estoque (com estorno automático de saldo)
- Cancelamento/estorno de Pedido com devolução ao estoque

**Integridade do Estoque** — PLANNED

- `select_for_update()` na reserva de estoque (corrige race condition)
- `transaction.atomic()` envolvendo toda mutação de saldo
- Validação de saldo negativo como constraint de banco
- Limpeza de arquivo de empenho ao cancelar pedido

**Permissões por Papel** — PLANNED

- Papéis: Almoxarife, Comprador/Fiscal, Solicitante (Secretaria), Administrador
- Almoxarife: acesso total a entradas e baixa
- Comprador/Fiscal: gestão de pedidos e empenhos
- Solicitante: apenas cria pedidos da própria secretaria
- Admin: configurações, cadastros e usuários

**Rastreabilidade de Usuário** — PLANNED

- Registrar `criado_por` e `modificado_por` em Entrada e Pedido
- Exibir responsável no detalhe do pedido e na listagem de entradas

---

## Milestone 3: Geração de Documentos & Relatórios Avançados

**Goal:** Documentos impressos para conformidade pública, relatórios filtráveis e exportação de dados
**Target:** Planejado

### Features

**Impressão e PDF** — PLANNED

- Guia de saída de material (Pedido em formato de documento assinável)
- Ficha de controle individual de produto (extrato completo de movimentação)
- Relatório de estoque em PDF para inventário oficial
- Geração via WeasyPrint ou xhtml2pdf

**Relatórios Avançados** — PLANNED

- Filtros por data (de/até), secretaria, categoria, status
- Exportação para CSV e XLSX (openpyxl)
- Histórico completo de movimentações por produto (página dedicada)
- Consumo por produto por período

**Importação de Licitação** — PLANNED

- Upload de planilha XLS/XLSX com itens licitados
- Validação de produtos cadastrados antes da importação
- Preview antes de confirmar a importação
- Substituir o placeholder atual (`importar_licitacao`)

---

## Milestone 4: Qualidade & Manutenibilidade

**Goal:** Cobertura de testes, refatoração estrutural e melhoria de DX
**Target:** Paralelo a outros milestones

### Features

**Cobertura de Testes** — PLANNED

- Testes de signals (mutação de estoque: reserva, entrega, cancelamento)
- Testes de views CRUD (criação, edição, deleção com ProtectedError)
- Testes de formulários (validações customizadas)
- Testes de permissões (quando Milestone 2 estiver pronto)

**Refatoração de views.py** — PLANNED

- Dividir `estoque/views.py` (533+ linhas) em pacote `views/`
- Módulos: `produtos.py`, `fornecedores.py`, `entradas.py`, `pedidos.py`, `relatorios.py`
- Dividir `estoque/tests.py` em pacote `tests/`

**Auditoria Completa** — PLANNED

- Log de todas as mutações de estoque (quem, quando, de quanto para quanto)
- Tela de auditoria para o Administrador
- Integração com `django-simple-history` ou log manual

---

## Milestone 5: Analytics & Produtividade

**Goal:** Dashboard com gráficos e operações em lote para alto volume
**Target:** Longo prazo

### Features

**Dashboard Analytics** — PLANNED

- Gráficos de consumo mensal por secretaria (Chart.js)
- Evolução do estoque por produto ao longo do tempo
- Alertas visuais configuráveis de estoque crítico

**Operações em Lote** — PLANNED

- Importação em massa de produtos via planilha
- Atualização em lote de estoque mínimo
- Processamento de múltiplos pedidos por secretaria

**Notificações** — PLANNED

- Alerta por email quando produto abaixo do estoque mínimo
- Resumo semanal de movimentações para o almoxarife

---

## Futuro / Fora de Escopo Atual

- API REST para integração com sistema contábil (SIG/e-cidade)
- App mobile para conferência de estoque em prateleiras
- Multi-exercício (separação de estoque por ano fiscal)
- Autenticação via LDAP/SSO municipal
