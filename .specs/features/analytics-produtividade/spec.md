# Analytics & Produtividade Specification

## Problem Statement

O dashboard atual exibe apenas KPIs estáticos (contagens e listas) sem visualização de tendências ou gráficos. O almoxarife não consegue identificar padrões de consumo ao longo do tempo nem distribuir operações em lote. Não há alertas proativos de estoque crítico — o operador precisa consultar manualmente.

## Goals

- [ ] Dashboard com gráficos interativos de consumo e distribuição
- [ ] Indicadores visuais de tendência (comparação mês a mês)
- [ ] Operações em lote para importação de produtos e atualização de estoque mínimo
- [ ] Alertas configuráveis de estoque crítico

## Out of Scope

| Feature | Reason |
| --- | --- |
| Gráfico de evolução de estoque por produto (time series real) | Exige tabela de histórico/auditoria que o sistema ainda não possui |
| Notificações por email | Sem infraestrutura de envio de email configurada; depende de SMTP |
| Processamento de múltiplos pedidos por secretaria | Requer redesign do fluxo de pedidos; adiado para v2 |
| Resumo semanal de movimentações | Depende de task queue/Celery; fora do escopo atual síncrono |
| Alertas visuais configuráveis pelo usuário | Complexidade extra — configuração de thresholds fica para iteração futura |

---

## User Stories

### P1: Dashboard com Gráficos e KPIs Melhorados

**User Story:** Como almoxarife, quero visualizar gráficos de consumo por secretaria e por categoria no dashboard para identificar padrões e tomar decisões de reposição com agilidade.

**Why P1:** É a funcionalidade de maior impacto imediato — transforma o dashboard de uma tela de "contagens" para uma ferramenta de análise visual.

**Acceptance Criteria:**

1. WHEN o usuário acessa o dashboard THEN o sistema SHALL exibir gráfico de barras com consumo mensal por secretaria (últimos 6 meses)
2. WHEN o usuário acessa o dashboard THEN o sistema SHALL exibir gráfico de pizza com distribuição de consumo por categoria (pedidos entregues)
3. WHEN o usuário acessa o dashboard THEN o sistema SHALL exibir indicadores KPI com variação percentual comparando mês atual vs mês anterior (pedidos realizados, entradas de estoque, itens consumidos)
4. WHEN o dashboard é carregado THEN os gráficos SHALL ser renderizados com Chart.js via CDN
5. WHEN não há dados de consumo para o período THEN os gráficos SHALL exibir mensagem "Sem dados no período"

**Independent Test:** Acessar o dashboard e verificar que 2 gráficos são renderizados com dados dos pedidos entregues e entradas existentes.

---

### P2: Operações em Lote

**User Story:** Como almoxarife, quero importar produtos em massa via planilha e atualizar estoque mínimo de vários produtos de uma vez para reduzir o tempo de operações repetitivas.

**Why P2:** Aumenta a produtividade em cenários de cadastro inicial e ajustes periódicos de parâmetros de estoque.

**Acceptance Criteria:**

1. WHEN o usuário faz upload de planilha XLSX com colunas [Nome, Categoria, Unidade, Estoque Mínimo] THEN o sistema SHALL exibir preview dos produtos a serem importados
2. WHEN o usuário confirma a importação THEN o sistema SHALL criar os produtos não existentes e pular duplicados (por nome exato)
3. WHEN o usuário seleciona múltiplos produtos na listagem THEN o sistema SHALL permitir atualização em lote do estoque mínimo via modal
4. WHEN a planilha contém linhas inválidas THEN o sistema SHALL exibir os erros no preview sem interromper o processamento das linhas válidas

**Independent Test:** Fazer upload de uma planilha com 5 produtos, confirmar, e verificar que aparecem na listagem de produtos.

---

### P3: Alertas de Estoque no Dashboard

**User Story:** Como almoxarife, quero ver alertas visuais destacados no dashboard quando produtos estão abaixo do estoque mínimo para agir antes da ruptura.

**Why P3:** Melhora a visibilidade de itens críticos mas não é essencial para a operação diária (o usuário já pode consultar a lista de estoque crítico).

**Acceptance Criteria:**

1. WHEN há produtos com estoque abaixo do mínimo THEN o dashboard SHALL exibir um banner de alerta com a contagem de itens críticos
2. WHEN o usuário clica no banner THEN o sistema SHALL redirecionar para o relatório de estoque filtrado por críticos
3. WHEN todos os produtos estão acima do estoque mínimo THEN o banner SHALL exibir mensagem "Estoque regular — sem itens críticos"

**Independent Test:** Criar um produto com estoque atual = 0 e estoque mínimo = 10; acessar o dashboard e ver o banner de alerta.

---

## Edge Cases

- WHEN não há pedidos entregues nos últimos 6 meses THEN o gráfico de consumo mostra eixos vazios com mensagem informativa
- WHEN um produto tem nome idêntico mas categoria diferente na importação em lote THEN o sistema SHALL tratá-lo como duplicado (match apenas por nome)
- WHEN a planilha de importação está vazia (apenas cabeçalhos) THEN o sistema SHALL exibir "Nenhum produto encontrado na planilha"
- WHEN o banco de dados não tem nenhum pedido THEN todos os gráficos SHALL exibir o estado vazio corretamente

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| DASH-01 | P1: Gráfico de consumo mensal por secretaria | Execute | Verified |
| DASH-02 | P1: Gráfico de pizza por categoria | Execute | Verified |
| DASH-03 | P1: KPIs com variação mensal (3 indicadores) | Execute | Verified |
| DASH-04 | P1: Integração Chart.js via CDN no base.html | Execute | Verified |
| DASH-05 | P1: Estado vazio para gráficos sem dados | Execute | Verified |
| BATCH-01 | P2: Upload e preview de planilha de produtos | Execute | Verified |
| BATCH-02 | P2: Importação com criação de produtos + skip de duplicados | Execute | Verified |
| BATCH-03 | P2: Atualização em lote de estoque mínimo | Execute | Verified |
| BATCH-04 | P2: Tratamento de erros na planilha (linhas inválidas) | Execute | Verified |
| ALERT-01 | P3: Banner de alerta com contagem de itens críticos | Execute | Verified |
| ALERT-02 | P3: Link do banner para relatório de estoque filtrado | Execute | Verified |
| ALERT-03 | P3: Banner verde quando sem itens críticos | Execute | Verified |

**Coverage:** 12 total, 12 mapped to tasks, 0 unmapped

---

## Success Criteria

- [x] O dashboard renderiza 2 gráficos (barras + pizza) com dados reais em < 1 segundo
- [x] Importação de 100 produtos via planilha conclui em < 3 segundos
- [x] Banner de alerta atualiza automaticamente quando estoque crítico é resolvido
