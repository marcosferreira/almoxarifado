# Architecture

**Pattern:** Monolithic Django app with single `estoque` app

## High-Level Structure

```
┌──────────────────────────────────────────────────┐
│                   nginx:alpine                    │
│  reverse proxy / static/media serving             │
└────────────┬──────────────────────────┬───────────┘
             │                          │
    /static/* /media/*           / → gunicorn
             │                          │
┌────────────┴──────────────────────────┴───────────┐
│                   Django App                       │
│                                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │            core (project package)             │  │
│  │  settings.py, urls.py, wsgi.py               │  │
│  └──────────────────────────────────────────────┘  │
│                      │                              │
│  ┌──────────────────────────────────────────────┐  │
│  │           estoque (single app)                │  │
│  │  models.py, views.py, forms.py, urls.py,      │  │
│  │  signals.py, admin.py, tests.py,              │  │
│  │  context_processors.py                        │  │
│  └──────────────────────────────────────────────┘  │
│                                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │              templates/                        │  │
│  │  base.html + estoque/* + registration/*       │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │    PostgreSQL 17     │
              └─────────────────────┘
```

## Identified Patterns

### Function-Based Views with Decorators

**Location:** `estoque/views.py`
**Purpose:** All views are function-based with `@login_required` decorator
**Implementation:** Standard request/response cycle with `render()`, `redirect()`, `get_object_or_404()`
**Example:** `views.py:108-115` — `produto_list()` function

### Signals for Domain Events

**Location:** `estoque/signals.py`
**Purpose:** Stock mutations (reserve/release/consume) are triggered via Django signals on model save
**Implementation:** `@receiver(post_save, sender=ItemEntrada)` and `@receiver(pre_save, sender=Pedido)`
**Critical flow:** Stock reservation happens in `gerenciar_fluxo_estoque` pre-save signal, comparing old vs new Pedido status

### ModelForm + InlineFormSet CRUD

**Location:** `estoque/forms.py`
**Purpose:** All CRUD forms use Django ModelForm with `inlineformset_factory` for parent-child (Entrada→ItemEntrada, Pedido→ItemPedido)
**Implementation:** Standard Django form pattern; parent form saved first, then formset instance attached
**Example:** `forms.py:166-171`

### Dynamic Dependent Selects

**Location:** `views.py:61-68` + `forms.py:78-92`
**Purpose:** Setor dropdown filters based on selected Unidade (and vice versa)
**Implementation:** AJAX endpoint (`/api/setores-por-unidade/`) + queryset override in `__init__` for server-side filtering on validation

### CSS Design Tokens with Theme Switching

**Location:** `static/css/design-tokens.css`
**Purpose:** Two UI themes (classic/modern) using `data-theme` attribute on `<body>`
**Implementation:** CSS custom properties on `:root` / `[data-theme="classic"]` and `[data-theme="modern"]`, toggled via user profile preference

## Data Flow

### Stock Entry Flow

```
User submits EntradaForm + ItemEntradaFormSet
    → entrada_create() saves Entrada, formset saves ItemEntrada instances
    → post_save signal on ItemEntrada triggers atualizar_estoque_entrada()
    → Produto.estoque_atual += quantidade for each item
```

### Stock Outflow (Pedido lifecycle)

```
1. Pedido created (status=SOLICITADO)
   → No stock mutation

2. User clicks "Reservar" → status=RESERVADO
   → pre_save signal: checks estoque_disponivel >= quantidade for each item
   → Raises ValueError if insufficient stock
   → Produto.estoque_reservado += quantidade

3. User uploads empenho PDF → status=EMPENHADO
   → File saved, status updated

4. User clicks "Confirmar Entrega" → status=ENTREGUE
   → pre_save signal:
     - If was RESERVADO or EMPENHADO:
       Produto.estoque_atual -= quantidade
       Produto.estoque_reservado -= quantidade
     - Else (direct flow):
       Produto.estoque_atual -= quantidade only

5. User clicks "Cancelar" → status=CANCELADO
   → If was RESERVADO or EMPENHADO:
     Produto.estoque_reservado -= quantidade (reverses reservation)
```

## Code Organization

**Approach:** Layer-based (models, views, forms, templates all separated by type)

**Module boundaries:**
| Layer | Location | Responsibility |
|---|---|---|
| Models | `estoque/models.py` | Data + business rules (properties) |
| Views | `estoque/views.py` | HTTP request handling |
| Forms | `estoque/forms.py` | Form/validation logic |
| Signals | `estoque/signals.py` | Side effects on save |
| Templates | `templates/estoque/` | HTML rendering |
| URLs | `estoque/urls.py` | Route definitions |
| Admin | `estoque/admin.py` | Django admin config |
| Config | `core/settings.py` | Django settings |
