# Code Conventions

## Naming Conventions

**Files:**
- Python: `snake_case.py` (e.g., `context_processors.py`, `produto_list.html`)
- Templates: `snake_case.html` (e.g., `fornecedor_form.html`, `pedido_detail.html`)
- Static: kebab-case (e.g., `design-tokens.css`, `ui.js`)

**Functions/Methods:**
- `snake_case` throughout
- Views prefixed by model name + action: `produto_list`, `produto_create`, `produto_update`
- Helper functions prefixed with underscore: `_to_decimal`
- Examples: `atualizar_estoque_entrada`, `gerenciar_fluxo_estoque`, `setores_por_unidade`

**Variables:**
- `snake_case` throughout
- Examples: `total_produtos`, `pedidos_reservados`, `old_instance`

**Models:**
- Singular `PascalCase`: `Produto`, `ItemEntrada`, `PerfilUsuario`
- Portuguese names throughout
- `class Meta` with `verbose_name` and `verbose_name_plural`

**URL names:**
- `snake_case` prefixed by model: `produto_list`, `fornecedor_create`, `pedido_detail`
- API endpoints prefixed with `/api/`: `api/setores-por-unidade/`

## Code Organization

**Imports:**
- stdlib first, then Django, then local
- No blank line groups in practice; `from .models import (...)` for local

**File Structure:**
- Models: class definitions, `class Meta` inside each, `__str__` method, `@property` for computed fields
- Views: import block, helper functions, then grouped by entity (commented `# --- PRODUTOS ---`)
- Forms: one class per model, `class Meta` with `fields` list and optional `widgets`, `__init__` for dynamic querysets

## Type Safety / Documentation

- No type hints anywhere in the codebase
- Docstrings only in auto-generated Django files (`core/settings.py`, `core/urls.py`)
- No docstrings in custom code

## Error Handling

- Django messages framework for user feedback (`messages.success`, `messages.error`)
- `ProtectedError` caught on delete for referential integrity
- `ValueError` raised in signals for business rule violations (insufficient stock)
- No custom exception classes
- No try/except on most operations

## Comments / Documentation

- Minimal comments in code
- Section headers in views: `# --- PRODUTOS ---`, `# --- ENTRADAS ---`
- Signal functions have inline comments explaining status transitions
- README.md documents functional requirements and installation
- External `docs/design-system.md` documents frontend architecture

## Template Conventions

- Tailwind CSS via CDN with `@layer base` and `@layer components` directives
- Alpine.js for interactivity (modals, sidebar toggle, tab switching)
- CSS custom properties for theming via `data-theme` attribute
- Emoji icons for navigation items
- Portuguese text throughout
