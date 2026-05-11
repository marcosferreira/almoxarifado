# Project Structure

**Root:** `/home/marcos/Ws/pmdonaines/smaf/almoxarifado`

## Directory Tree

```
almoxarifado/
├── core/                     # Django project package
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── estoque/                  # Single Django app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html             # Main shell layout
│   ├── index.html            # Legacy/alt dashboard
│   ├── components/
│   │   └── action_sidebar_standard.html
│   ├── estoque/              # Per-feature templates
│   │   ├── dashboard.html
│   │   ├── entrada_form.html
│   │   ├── entrada_list.html
│   │   ├── fornecedor_form.html
│   │   ├── fornecedor_list.html
│   │   ├── importar_licitacao.html
│   │   ├── pedido_detail.html
│   │   ├── pedido_form.html
│   │   ├── pedido_list.html
│   │   ├── produto_form.html
│   │   ├── produto_list.html
│   │   ├── relatorio_estoque.html
│   │   ├── relatorio_pedidos.html
│   │   ├── relatorios.html
│   │   ├── setor_form.html
│   │   ├── setor_list.html
│   │   ├── unidade_form.html
│   │   └── unidade_list.html
│   └── registration/
│       ├── login.html
│       └── profile.html
├── static/
│   ├── css/design-tokens.css
│   ├── js/ui.js
│   └── images/logo.png
├── staticfiles/              # Collectstatic output
├── media/                    # User uploads (empenhos)
├── nginx/
│   └── default.conf
├── docs/
│   ├── design-system.md
│   ├── README.md
│   └── assets/               # Screenshots, docx, xlsx
├── Dockerfile
├── docker-compose.yaml
├── docker-compose.dev.yml
├── entrypoint.sh
├── pyproject.toml
├── .env.template
├── .python-version
├── .gitignore
├── manage.py
├── genkey.py
└── README.md
```

## Module Organization

### `core/` — Django Project Config

**Purpose:** Settings, root URL routing, WSGI/ASGI entrypoints
**Location:** `core/`
**Key files:** `settings.py`, `urls.py`

### `estoque/` — Business Logic (single app)

**Purpose:** Full inventory management — models, views, forms, signals, admin
**Location:** `estoque/`
**Key files:** `models.py`, `views.py`, `signals.py`, `forms.py`

### `templates/` — HTML Views

**Purpose:** All server-rendered templates
**Key files:** `base.html` (shell), `estoque/pedido_detail.html` (critical workflow)

### `static/` — Frontend Assets

**Purpose:** CSS design tokens, JS UI helpers, images
**Key files:** `css/design-tokens.css` (theme system), `js/ui.js` (keyboard shortcuts)

### Infrastructure

| Directory | Purpose |
|---|---|
| `nginx/` | Reverse proxy config for production |
| `docs/` | Design system doc + reference assets |
| `staticfiles/` | Collectstatic output (gitignored, Docker-generated) |
| `media/` | User-uploaded empenho PDFs |

## Where Things Live

| Capability | Location |
|---|---|
| Data models | `estoque/models.py` |
| HTTP handlers | `estoque/views.py` |
| Form validation | `estoque/forms.py` |
| Side effects (stock) | `estoque/signals.py` |
| Admin interface | `estoque/admin.py` |
| URL routing | `core/urls.py` + `estoque/urls.py` |
| HTML templates | `templates/estoque/` |
| Theme/design tokens | `static/css/design-tokens.css` |
| Docker orchestration | `docker-compose.yaml` |
