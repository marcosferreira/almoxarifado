# 📦 Almoxarifado - Prefeitura Municipal de Dona Inês

Sistema de gestão de almoxarifado completo para a Prefeitura Municipal de Dona Inês, focado no controle de entradas e saídas do setor de compras, com fluxo de integração com a contabilidade via empenho.

## 🚀 Tecnologias

Este projeto utiliza uma stack moderna baseada em Python e Django, focada em produtividade e manutenibilidade.

- **Backend:** [Django 6.x](https://www.djangoproject.com/)
- **Frontend:** [Django Templates](https://docs.djangoproject.com/en/5.1/topics/templates/), [Tailwind CSS](https://tailwindcss.com/) e [AlpineJS](https://alpinejs.dev/)
- **Gerenciador de Pacotes:** [uv](https://github.com/astral-sh/uv)
- **Configuração:** [python-dotenv](https://github.com/theskumar/python-dotenv)

## 🎛️ Temas de UI por Usuário

O sistema agora possui tema de interface por perfil de usuário:

- `classic`: mantém o visual ERP tradicional.
- `modern`: visual atualizado com tokens de design e melhor contraste.

Como usar:

1. Acesse `Perfil` no cabeçalho.
2. Altere `Tema da Interface`.
3. Salve os dados para persistir a preferência no perfil.

Notas técnicas:

- A preferência é salva em `PerfilUsuario.tema_ui`.
- Usuários existentes recebem perfil automaticamente pela migração de backfill.

## 📋 Requisitos Funcionais (RF)

O sistema deve atender às seguintes funcionalidades essenciais:

- **RF01 - Autenticação e Autorização:** Controle de acesso nativo do Django (Usuários, Grupos e Permissões).
- **RF02 - Cadastro de Fornecedores:** Gestão de parceiros comerciais que fornecem materiais para a prefeitura.
- **RF03 - Gestão de Produtos:** Cadastro detalhado de itens com categorias, unidades de medida e controle de estoque mínimo.
- **RF04 - Entrada de Estoque:** Registro de compras e doações, atualizando o saldo disponível imediatamente.
- **RF05 - Pedidos de Saída (Requisições):** Interface para secretarias solicitarem materiais do almoxarifado.
- **RF06 - Agendamento de Baixa:** Reserva automática de produtos no estoque ao criar um pedido, evitando duplicidade de saída.
- **RF07 - Anexação de Empenho:** Fluxo obrigatório onde a baixa efetiva do estoque só ocorre após a anexação do documento de empenho da contabilidade.
- **RF08 - Baixa Efetiva de Estoque:** Atualização definitiva do estoque após a confirmação do empenho.
- **RF09 - Histórico e Logs:** Auditoria de todas as movimentações de entrada e saída.
- **RF10 - Relatórios:** Geração de inventários e relatórios de consumo por secretaria.

## 🔄 Fluxo de Baixa de Pedido

Diferente de sistemas convencionais, este almoxarifado segue um fluxo de conformidade pública:

1. **Solicitação:** A secretaria realiza o pedido de materiais.
2. **Reserva (Agendamento):** O sistema reserva os itens, diminuindo o saldo "disponível" mas mantendo o saldo "físico".
3. **Empenho:** O setor de compras/contabilidade processa o empenho e o arquivo PDF/imagem é anexado ao pedido no sistema.
4. **Baixa Efetiva:** Uma vez anexado o empenho, o almoxarife confirma a entrega e o sistema realiza a baixa física definitiva do estoque.

## 🛠️ Instalação e Configuração

Certifique-se de ter o `uv` instalado em sua máquina.

1. **Clonar o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd almoxarifado
   ```

2. **Configurar o ambiente:**
   ```bash
   uv sync
   ```

3. **Configurar variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto (use o `.env.example` se disponível):
   ```env
   DEBUG=True
   SECRET_KEY=django-insecure-sua-chave-aqui
   DATABASE_URL=sqlite:///db.sqlite3
   ```

4. **Executar migrações e servidor:**
   ```bash
   uv run python manage.py migrate
   uv run python manage.py runserver
   ```

## 🎨 Desenvolvimento de Frontend

Para compilar o Tailwind CSS (caso esteja usando o CLI do Tailwind):
```bash
# Exemplo se usar tailwindcss stand-alone ou via npm
npm install
npm run dev
```

## 📄 Licença

Este projeto é de uso exclusivo da Prefeitura Municipal de Dona Inês.
