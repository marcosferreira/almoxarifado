# Testing Infrastructure

## Test Frameworks

**Unit/Integration:** Django TestCase (built-in, no external test libraries)
**Coverage:** Not configured

## Test Organization

**Location:** `estoque/tests.py`
**Naming:** Single `tests.py` file (not a package), class names end with `Tests`, methods prefixed with `test_`
**Structure:** Flat file, one test class currently

## Testing Patterns

### Unit/Integration Tests

**Approach:** Django TestCase with `@override_settings` for staticfiles storage
**Location:** `estoque/tests.py`
**Current tests:**
- `PerfilUsuarioTemaTests` — 3 tests covering profile auto-creation, theme persistence, and theme rendering in templates

### Coverage Gaps

- No tests for stock entry flow (Entrada + ItemEntrada signals)
- No tests for Pedido lifecycle (reserve → empenho → entregue → cancelado)
- No tests for stock reservation validation (insufficient stock)
- No tests for CRUD views
- No tests for forms or form validation
- No tests for admin configuration

## Test Execution

**Commands:** `uv run python manage.py test`
**Configuration:** Uses default Django test runner with SQLite in-memory database

## Coverage Targets

**Current:** ~5% (3 tests covering profile/theme only)
**Goals:** Not documented
**Enforcement:** None

## Test Coverage Matrix

| Code Layer | Required Test Type | Location Pattern | Run Command |
|---|---|---|---|
| Models (business logic) | unit | `estoque/tests.py` | `uv run python manage.py test` |
| Signals (stock mutation) | integration | `estoque/tests.py` | `uv run python manage.py test` |
| Views (CRUD) | integration | `estoque/tests.py` | `uv run python manage.py test` |
| Forms (validation) | unit | `estoque/tests.py` | `uv run python manage.py test` |
| Templates (rendering) | integration | `estoque/tests.py` | `uv run python manage.py test` |

## Parallelism Assessment

| Test Type | Parallel-Safe? | Isolation Model | Evidence |
|---|---|---|---|
| Current tests | Yes | Default TestCase (DB transactions per test) | No shared state, no globals |

## Gate Check Commands

| Gate Level | When to Use | Command |
|---|---|---|
| Quick | After tasks with unit tests only | `uv run python manage.py test -v 2` |
| Full | After tasks with integration tests | `uv run python manage.py test -v 2` |
| Build | After phase completion | `uv run python manage.py check --deploy` + test |
