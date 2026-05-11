# Almoxarifado — Prefeitura Municipal de Dona Inês

**Vision:** Sistema de gestão de almoxarifado completo para controle de entradas, saídas e fluxo de empenho contábil da Prefeitura Municipal de Dona Inês.
**For:** Setor de Compras e Almoxarifado da Prefeitura
**Solves:** Controle de estoque com fluxo de conformidade pública — a baixa física do estoque só ocorre após anexação do empenho contábil.

## Goals

- Gerenciar todo o ciclo de vida de materiais: cadastro → entrada → reserva → empenho → baixa
- Garantir auditoria e rastreabilidade de todas as movimentações de estoque
- Fornecer relatórios de inventário, consumo por secretaria e status de pedidos
- Interface operacional produtiva com atalhos de teclado e tema clássico ERP

## Tech Stack

**Core:**
- Framework: Django 6.0.4
- Language: Python 3.12
- Database: PostgreSQL 17 (production), SQLite (dev)

**Key dependencies:** psycopg 3, gunicorn, whitenoise, dj-database-url, python-dotenv, Tailwind CSS, Alpine.js

## Scope

**v1 includes:**
- Cadastro de produtos, fornecedores, unidades e setores
- Entrada de estoque com notas fiscais e licitações
- Pedidos de saída com fluxo Solicitar → Reservar → Empenhar → Entregar → Cancelar
- Anexação de empenho (PDF) como gate para baixa efetiva
- Dashboard com indicadores e alertas de estoque crítico
- Relatórios de movimento, estoque e pedidos
- Dois temas de interface (classic e modern) por perfil de usuário
- Importação de licitação (placeholder)
- Autenticação via Django auth

**Explicitly out of scope:**
- API REST (sem DRF)
- Integração com sistemas externos (SIG, contabilidade)
- Notificações por email
- App mobile
- Autenticação via LDAP/OAuth
- Geração de empenho (o sistema apenas anexa)

## Constraints

- **Technical:** Docker-based deployment (app + nginx + postgres), sem task queue (tudo síncrono)
- **Infrastructure:** Servidor único, sem escalabilidade horizontal planejada
- **Data integrity:** Estoque é recurso crítico — race conditions podem causar saldo negativo
