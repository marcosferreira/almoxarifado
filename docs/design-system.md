# Design System Atual (As-Is)

## 1) Contexto e stack

- Projeto web server-rendered com Django Templates.
- Styling com Tailwind CSS via CDN (`https://cdn.tailwindcss.com`) e customizacao inline em `templates/base.html`.
- Interacoes leves com Alpine.js via CDN (`https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js`).
- Nao ha pipeline de assets frontend ativo no repositorio atual (sem arquivos CSS/JS em `static/` no momento da analise).

Referencias:
- `templates/base.html`
- `README.md`

## 2) Arquitetura visual geral

O sistema adota uma linguagem visual inspirada em ERP/classico desktop:

- Cores frias (azuis e cinzas) como base de toda a interface.
- Estrutura em "janelas" com barra de titulo.
- Tabelas densas com tipografia pequena (11px/12px).
- Barra lateral de acoes com botoes padronizados e atalhos de teclado (F2-F8, Esc).
- Modais no mesmo idioma visual das telas principais.

O layout principal esta em `templates/base.html`:

- Header superior com dados da entidade e usuario.
- Sidebar esquerda com navegacao por blocos (`details/summary`).
- Area principal de conteudo.
- Sidebar direita de suporte (visivel em `xl`).

## 3) Fundacoes (tokens e estilos base)

## 3.1 Tipografia

- Familia global: `"Segoe UI", Tahoma, sans-serif`.
- Escalas mais usadas:
  - `text-[9px]`, `text-[10px]`, `text-[11px]`, `text-[12px]`, `text-[13px]`
  - Casos pontuais: `text-lg`, `text-2xl`, `text-4xl`, `text-xl`
- Uso recorrente de `uppercase` e `font-bold`/`font-semibold` para carater de sistema operacional/ERP.

Fonte de definicao:
- `templates/base.html:70`

## 3.2 Cores

Nao ha design tokens nomeados em variaveis CSS; as cores sao aplicadas majoritariamente como valores inline do Tailwind (`bg-[#...]`, `text-[#...]`, `border-[#...]`).

### Paleta principal identificada

- Fundos estruturais:
  - `#b6c3dd` (fundo geral)
  - `#b9c7df` (painel/janela)
  - `#e7edf7` (sidebar suporte)
- Bordas e contornos:
  - `#7f9db9`, `#8ea6c8`, `#8ca5c9`, `#8aa1c2`, `#9bb1ce`, `#c2d1e7`, `#d4deef`
- Titulos e textos de destaque:
  - `#16345b`, `#17355d`, `#1a365d`, `#1d3a5f`, `#21416b`, `#243c5a`, `#27486f`, `#2c5586`
- Superficies auxiliares:
  - `#dfe8f5`, `#bacce8`, `#dbe6f8`, `#eef4ff`, `#f0f5ff`, `#dce6f7`, `#e9f0ff`, `#d8efe3`
- Acoes/estado:
  - Azul forte: `#0d3892`, `#0d43b8`
  - Vermelho alerta: `text-red-700`
  - Overlay modal: `#233a58` com opacidade (`/45`)

### Cores utilitarias Tailwind (sem hex explicito no codigo)

- `gray-*`, `blue-*`, `green-*`, `yellow-*`, `indigo-*`, `red-*`, `amber-*` usadas em badges, estados e telas de login/index.

## 3.3 Espacamento e dimensoes

- Espacamento predominante com utilitarios Tailwind curtos (`p-2`, `p-3`, `gap-2`, `gap-3`).
- Altura de header fixa: `h-10`.
- Sidebar principal: `w-64`.
- Sidebar de acoes recorrente: `xl:w-40`.
- Larguras tabeladas com `w-*` para colunas (ex.: `w-12`, `w-24`, `w-36`).

## 3.4 Bordas, raios e sombra

- Bordas 1px em quase todos os componentes (`border`).
- Raios pequenos (`rounded`, `rounded-md`) e pouca curvatura.
- Sombras discretas (`shadow-sm`) e shadow inset em `window-panel` para efeito classico.

## 3.5 Movimento e transicao

- Transicoes curtas (`transition`, `duration-150`, `duration-200`).
- Hover de linha em tabelas e botoes.
- Modais e sidebar com abertura/fechamento controlados por Alpine.

## 4) Componentes reutilizaveis

## 4.1 Base de componentes em `templates/base.html`

Classes de componente definidas em `@layer components`:

- `.btn-erp`
  - Botao em estilo bloco com icone/legenda (presente na base, uso pratico reduzido).
- `.window-panel`
  - Contenedor principal de "janela" com borda azul e fundo classico.
- `.window-title`
  - Barra de titulo com gradiente e tipografia de destaque.
- `.section-box`
  - Bloco interno para formularios/filtros.
- `.action-btn`
  - Principal CTA do sistema (barra lateral e acoes de tela).
- `.erp-modal-overlay`, `.erp-modal-window`, `.erp-modal-titlebar`, `.erp-modal-body`
  - Sistema de modal padronizado.

Fonte:
- `templates/base.html:32`

## 4.2 Form controls base

Definidos em `@layer base`:

- Inputs text/number/password/email/url/date/datetime-local, `select`, `textarea` recebem o mesmo padrao visual.
- `input[type="checkbox"]` customizado.
- `input[type="file"]` com estilo de botao para seletor de arquivo.
- `label` com uppercase, peso forte e tracking reduzido.

Fonte:
- `templates/base.html:10`

## 4.3 Sidebar de acoes padrao

Componente reutilizavel:
- `templates/components/action_sidebar_standard.html`

Acoes previstas:
- Salvar (F7)
- Incluir (F2)
- Alterar (F3)
- Excluir (F4)
- Consulta (F5)
- Cancelar (F6)
- Imprimir (F8)
- Fechar (Esc)

Suporta `url`, `click` (Alpine) e `onclick` por acao.

## 5) Padroes de layout e pagina

## 5.1 Shell da aplicacao

- Header fixo superior visualmente (nao `position: fixed`, mas com altura fixa).
- Navegacao lateral em acordeoes (`details`) por modulo:
  - Principal
  - Cadastros
  - Movimentacao
  - Relatorios
  - Diversos
- Conteudo principal com largura fluida.
- Sidebar de suporte em `xl`.

Arquivo:
- `templates/base.html`

## 5.2 Telas de lista (CRUD)

Padrao recorrente em:
- `templates/estoque/fornecedor_list.html`
- `templates/estoque/produto_list.html`
- `templates/estoque/pedido_list.html`
- `templates/estoque/entrada_list.html`

Estrutura comum:
- `window-panel` + `window-title`
- area de filtro (`section-box`)
- tabela principal com cabecalho azul claro
- barra lateral com `action-btn`

## 5.3 Telas de formulario

Padrao em:
- `templates/estoque/fornecedor_form.html`
- `templates/estoque/produto_form.html`
- `templates/estoque/pedido_form.html`
- `templates/estoque/entrada_form.html`
- `templates/registration/profile.html`

Estrutura comum:
- formulario em `section-box`
- agrupamentos por grid responsivo
- mensagens de erro pequenas em vermelho
- acoes na lateral direita

## 5.4 Modais

Presentes principalmente em:
- `templates/estoque/fornecedor_list.html`
- `templates/estoque/produto_list.html`
- `templates/estoque/pedido_form.html`
- `templates/estoque/entrada_form.html`

Padrao:
- overlay com fundo escurecido
- janela central com barra de titulo
- conteudo em `section-box` + tabela auxiliar

## 5.5 Dashboard e relatorios

- `templates/estoque/dashboard.html`: cards de resumo + tabelas operacionais + coluna de atalho.
- `templates/estoque/relatorios.html`: filtros + duas tabelas analiticas.

## 5.6 Autenticacao

- `templates/registration/login.html` usa visual distinto (mais moderno e simplificado), com fundo azul escuro e card branco.
- Diverge do padrao "ERP classico" adotado no restante do sistema.

## 6) Interacao e comportamento

## 6.1 Alpine.js

Usado para:
- controle de abertura de sidebar mobile (`base.html`)
- modais de consulta/insercao
- alternancia de abas (`profile.html`)
- calculos em tempo real nas tabelas de itens (`pedido_form.html`, `entrada_form.html`)

## 6.2 Teclado / produtividade

Existe padrao forte de atalhos:
- F2 Incluir
- F3 Alterar
- F4 Excluir
- F5 Consulta
- F6 Cancelar
- F7 Salvar
- F8 Imprimir
- Esc Fechar/voltar

Implementacao feita por `window.addEventListener('keydown', ...)` em varias telas.

## 7) Inventario de telas e componentes por arquivo

## 7.1 Base e shell

- `templates/base.html`
  - Shell principal (header, sidebars, conteudo)
  - Tokens/composicoes CSS inline
  - Componentes utilitarios do sistema

## 7.2 Componentes compartilhados

- `templates/components/action_sidebar_standard.html`
  - Sidebar padrao de acoes rapidas

## 7.3 Estoque

- `templates/estoque/dashboard.html`
  - Resumo operacional, listas de pedidos/entradas, blocos de pendencias
- `templates/estoque/fornecedor_list.html`
  - Lista + filtro + modal consulta
- `templates/estoque/fornecedor_form.html`
  - Formulario cadastro/edicao fornecedor
- `templates/estoque/produto_list.html`
  - Lista + filtro + modal consulta
- `templates/estoque/produto_form.html`
  - Formulario cadastro/edicao produto
- `templates/estoque/pedido_list.html`
  - Lista com filtros por status
- `templates/estoque/pedido_form.html`
  - Formulario completo + tabela de itens + calculos + modais
- `templates/estoque/pedido_detail.html`
  - Visualizacao/gestao do pedido e fluxo de empenho/entrega
- `templates/estoque/entrada_list.html`
  - Lista de entradas
- `templates/estoque/entrada_form.html`
  - Formulario de entrada + itens + calculos + modais
- `templates/estoque/importar_licitacao.html`
  - Tela de importacao com upload e acoes auxiliares
- `templates/estoque/relatorios.html`
  - Filtros e tabelas de analise

## 7.4 Outras telas

- `templates/registration/login.html`
  - Autenticacao
- `templates/registration/profile.html`
  - Perfil com abas de dados e senha
- `templates/index.html`
  - Dashboard alternativo/legado com estilo diferente do padrao atual

## 8) Convencoes visuais observadas

- Predominio de tabelas para apresentacao de dados transacionais.
- Blocos de formulario com titulo interno (`window-title` dentro de `section-box`).
- Linguagem iconografica por emoji em botoes/menu.
- Forte presenca de `uppercase` em cabecalhos e labels.
- Densidade informacional alta e foco em produtividade operacional.

## 9) Inconsistencias e oportunidades de padronizacao

## 9.1 Tokens

- Ausencia de variaveis CSS (cores, espacamento, tipografia, sombras).
- Muitas cores hardcoded em classes Tailwind arbitrarias (`[#hex]`).

## 9.2 Divergencia de linguagem entre telas

- `registration/login.html` e `index.html` destoam da linguagem ERP classica dominante.

## 9.3 Repeticao de comportamento JS

- Handlers de teclado repetidos em varios arquivos (risco de divergencia funcional).

## 9.4 Niveis de abstração

- Existe bom inicio de componentizacao (`action_sidebar_standard` e classes base), mas ainda com repeticao de blocos de tabela/filtro/modal.

## 10) Recomendacoes (proximo passo)

Para evoluir este design system sem quebrar o legado visual:

1. Introduzir tokens CSS em `:root` (cores, espacamentos, tipografia, bordas, sombras), mantendo alias para a paleta atual.
2. Consolidar componentes compartilhados em includes (ex.: tabela padrao, cabecalho de modulo, bloco de filtros).
3. Centralizar atalhos de teclado e utilitarios Alpine em um arquivo JS comum (quando houver pipeline de static).
4. Alinhar telas fora do padrao (login/index) para o mesmo idioma visual, ou documentar oficialmente excecoes.
5. Criar guia visual incremental com exemplos de uso por componente (botao, tabela, form, modal, status badge).

## 11) Assets de referencia

Capturas e arquivos auxiliares disponiveis em:

- `docs/assets/01.jpeg`
- `docs/assets/02.jpeg`
- `docs/assets/03.jpeg`
- `docs/assets/04.jpeg`
- `docs/assets/05.jpeg`
- `docs/assets/06.jpeg`
- `docs/assets/tela-pedidos-com-sidebar-completa.jpeg`
- `docs/assets/PRINT DO SISTEMA.docx`
- `docs/assets/PROPOSTA_ATUALIZADA-merenda-2026.xlsx`

---

Documento gerado a partir da analise do codigo-fonte atual dos templates e estilos inline do projeto.
