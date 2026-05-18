# Roadmap

**Current Milestone:** Analytics & Produtividade
**Status:** In Progress

---

## Milestone 1: Core Inventory Management ✅

**Goal:** Full inventory cycle — cadastro, entrada, saída com fluxo de empenho, relatórios básicos
**Target:** Shipped (2026-05-13)

### Features

**Autenticação e Perfis** — DONE

- Login/logout via Django auth
- Perfil de usuário com seleção de tema de interface
- Troca de senha pelo perfil

**Cadastros Base** — DONE

- CRUD completo de Unidades/Secretarias e Setores
- CRUD completo de Produtos (categoria, unidade, estoque mínimo)
- CRUD completo de Fornecedores (CNPJ, contato)
- Vínculo de produtos a fornecedores

**Entrada de Estoque** — DONE

- Entrada com nota fiscal, licitação, lote, programa, empenho
- Itens com quantidade e preço unitário
- Atualização automática de estoque via signal
- Suporte a compra direta e licitação

**Saída (Pedidos)** — DONE

- Criação de pedido com múltiplos itens
- Fluxo: Solicitado → Reservado → Empenhado → Entregue → Cancelado
- Reserva de estoque com validação de saldo disponível
- Anexação de empenho PDF como gate obrigatório
- Baixa efetiva do estoque na confirmação de entrega
- Cancelamento com liberação automática de reserva

**Relatórios Básicos** — DONE

- Relatório de Movimento (consumo por secretaria, entradas por categoria)
- Relatório de Estoque (atual, crítico, disponível, mínimo)
- Relatório de Pedidos (resumo por status, totais solicitado/atendido)

**UI / Tema** — DONE

- Dual theme system (classic ERP / modern)
- Design tokens via CSS custom properties
- Keyboard shortcuts (F2-F8, Esc)

---

## Milestone 2: CRUD Completion & Data Integrity ✅

**Goal:** Fechar lacunas de CRUD, eliminar race conditions e garantir integridade do estoque
**Target:** Shipped (2026-05-13)

### Features

**CRUD Completo** — DONE

- Exclusão de Produto (com proteção se houver movimentações)
- Edição e exclusão de Fornecedor
- Edição e exclusão de Entrada de Estoque (com estorno automático de saldo)
- Cancelamento/estorno de Pedido com devolução ao estoque

**Integridade do Estoque** — DONE

- `select_for_update()` na reserva de estoque (corrige race condition)
- `transaction.atomic()` envolvendo toda mutação de saldo
- Validação de saldo negativo como constraint de banco
- Limpeza de arquivo de empenho ao cancelar pedido

**Permissões por Papel** — DONE

- Papéis: Almoxarife, Comprador/Fiscal, Solicitante (Secretaria), Administrador
- Almoxarife: acesso total a entradas e baixa
- Comprador/Fiscal: gestão de pedidos e empenhos
- Solicitante: apenas cria pedidos da própria secretaria
- Admin: configurações, cadastros e usuários

**Rastreabilidade de Usuário** — DONE

- Registrar `criado_por` e `modificado_por` em Entrada e Pedido
- Exibir responsável no detalhe do pedido e na listagem de entradas

---

## Milestone 3: Geração de Documentos & Relatórios Avançados ✅

**Goal:** Documentos impressos para conformidade pública, relatórios filtráveis e exportação de dados
**Target:** Shipped (2026-05-14)

### Features

**Impressão e PDF** — DONE

- Guia de saída de material (Pedido em formato de documento assinável)
- Ficha de controle individual de produto (extrato completo de movimentação)
- Relatório de estoque em PDF para inventário oficial
- Geração via WeasyPrint

**Relatórios Avançados** — DONE

- Filtros por data (de/até), secretaria, categoria, status
- Exportação para CSV e XLSX (openpyxl)
- Histórico completo de movimentações por produto (página dedicada)
- Consumo por produto por período

**Importação de Licitação** — DONE

- Upload de planilha XLS/XLSX com itens licitados
- Validação de produtos cadastrados antes da importação
- Preview antes de confirmar a importação
- Substituição do placeholder (`importar_licitacao`)

---

## Milestone 4: Qualidade & Manutenibilidade ✅

**Goal:** Cobertura de testes, refatoração estrutural e melhoria de DX
**Target:** Shipped (2026-05-14)

### Features

**Cobertura de Testes** — DONE

- Testes de signals (mutação de estoque: reserva, entrega, cancelamento)
- Testes de views CRUD (criação, edição, deleção com ProtectedError)
- Testes de formulários (validações customizadas)
- Testes de permissões

**Refatoração de views.py** — DONE

- Dividir `estoque/views.py` (533+ linhas) em pacote `views/`
- Módulos: `produtos.py`, `fornecedores.py`, `entradas.py`, `pedidos.py`, `relatorios.py`
- Dividir `estoque/tests.py` em pacote `tests/`

**Auditoria Completa** — DONE

- Log de todas as mutações de estoque (quem, quando, de quanto para quanto)
- Tela de auditoria para o Administrador
- Integração com `django-simple-history`

---

## Milestone 5: Analytics & Produtividade

**Goal:** Dashboard com gráficos e operações em lote para alto volume
**Target:** In Progress (2026-05-15)

### Features

**Dashboard Analytics** — DONE

- Gráficos de consumo mensal por secretaria (Chart.js)
- Gráfico de pizza de consumo por categoria
- Indicadores de performance (KPIs) com variação mensal no dashboard
- Banner de alerta de estoque crítico com link para relatório

**Operações em Lote** — DONE

- Importação em massa de produtos via planilha XLSX com preview
- Atualização em lote de estoque mínimo via listagem de produtos
- Processamento de múltiplos pedidos por secretaria (adiado para v2)

**Notificações** — PLANNED

- Alerta por email quando produto abaixo do estoque mínimo
- Resumo semanal de movimentações para o almoxarife

---

## Futuro / Fora de Escopo Atual

- API REST para integração com sistema contábil (SIG/e-cidade)
- App mobile para conferência de estoque em prateleiras
- Multi-exercício (separação de estoque por ano fiscal)
- Autenticação via LDAP/SSO municipal
