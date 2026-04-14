# ♊ GEMINI.md - Contexto do Projeto Almoxarifado

Este arquivo fornece diretrizes e contexto essencial para o Gemini CLI atuar no projeto Almoxarifado da Prefeitura Municipal de Dona Inês.

## 📌 Visão Geral do Projeto

O sistema é uma aplicação Django Fullstack para gerenciar entradas e saídas de materiais. O diferencial é o fluxo de conformidade pública, onde a baixa física do estoque só ocorre após a anexação do empenho contábil.

- **Nome:** Almoxarifado
- **Propósito:** Gestão de suprimentos e controle de estoque com reserva (agendamento) e confirmação via empenho.
- **Público:** Prefeitura Municipal de Dona Inês (Setor de Compras e Almoxarifado).

## 🛠️ Stack Tecnológica

- **Linguagem:** Python 3.12+
- **Framework Web:** Django 6.x
- **Frontend:** Django Templates + Tailwind CSS + AlpineJS.
- **Gerenciador de Dependências:** [uv](https://github.com/astral-sh/uv).
- **Ambiente:** `python-dotenv` para variáveis de ambiente.

## 🏗️ Arquitetura e Fluxo de Dados

### Entidades Principais (Sugestão de Modelos)
- **Produto:** Nome, categoria, unidade de medida, estoque atual, estoque reservado, estoque mínimo.
- **Fornecedor:** Dados cadastrais.
- **Movimentação (Entrada):** Origem, fornecedor, itens, data.
- **Pedido (Saída):** Secretaria solicitante, status (Solicitado, Reservado, Empenhado, Entregue), anexo de empenho.
- **ItemPedido:** Produto, quantidade, preço unitário (se disponível).

### Fluxo Crítico: Saída de Material
1. **Solicitação:** Criação do Pedido.
2. **Reserva:** Ao salvar o pedido como 'Reservado', o sistema deve atualizar `Produto.estoque_reservado`. O `estoque_disponivel` é calculado como `estoque_atual - estoque_reservado`.
3. **Anexação de Empenho:** O status muda para 'Empenhado'.
4. **Entrega/Baixa:** Ao confirmar a entrega, `estoque_atual` é decrementado e `estoque_reservado` é limpo para aquele pedido.

## 🚀 Comandos Úteis

### Gerenciamento com `uv`
- Instalar dependências: `uv sync`
- Adicionar pacote: `uv add <pacote>`
- Rodar comando python: `uv run python <comando>`

### Django (via `uv run`)
- Migrations: `uv run python manage.py makemigrations` / `migrate`
- Servidor: `uv run python manage.py runserver`
- Shell: `uv run python manage.py shell`

## 🎨 Convenções de Desenvolvimento

- **CSS:** Use Tailwind CSS via classes utilitárias diretamente nos templates.
- **JS:** Use AlpineJS para interações leves no frontend (modais, abas, filtros dinâmicos).
- **Configurações:** Mantenha segredos no `.env`. Nunca versione o `.env`.
- **Nomenclatura:** Variáveis e métodos em `snake_case` (padrão Python/Django). Templates em `kebab-case`.

## 📝 TODO / Próximos Passos

1. [ ] Inicializar o projeto Django (`django-admin startproject core .`).
2. [ ] Criar a app `estoque` ou `almoxarifado`.
3. [ ] Configurar o Tailwind CSS.
4. [ ] Implementar os modelos básicos seguindo o fluxo de empenho.
