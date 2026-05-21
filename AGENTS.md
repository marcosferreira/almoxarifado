# AGENTS.md — Almoxarifado (Prefeitura de Dona Inês)

## Critical: All commands run inside Docker

**Never run Python, Django, or database commands directly on the host.**
Always use `docker compose -f docker-compose.dev.yml exec app <cmd>` or the Makefile shortcuts.

```bash
# Preferred: use Makefile (always targets docker-compose.dev.yml)
make migrate
make makemigrations ARGS=estoque
make test
make test ARGS=estoque.tests.test_signals
make createsuperuser
make collectstatic
make dbshell
make bash-app        # interactive shell in container

# Equivalent raw docker compose
docker compose -f docker-compose.dev.yml exec app python manage.py migrate
docker compose -f docker-compose.dev.yml exec app python manage.py test estoque.tests.test_signals
```

> See `Makefile` for all available targets. Override compose file with `make COMPOSE_FILE=docker-compose.yaml <target>`.

## Package manager: uv (not pip)

```bash
uv sync            # install deps
uv add <package>   # add dependency
```

No `requirements.txt` — dependencies live in `pyproject.toml` + `uv.lock`.

## Start / stop dev environment

```bash
make up-d     # start in background
make down     # stop and remove containers
make rebuild  # rebuild image and restart
make logs-f   # follow logs
```

## Running tests

```bash
make test                              # all tests
make test ARGS=estoque.tests.test_pdf  # single module
```

No pytest — Django's built-in runner only.

## Language and naming conventions

- **All code, models, fields, URLs, views, and comments are in Brazilian Portuguese.**
- No type hints (unless explicitly asked).
- No docstrings in custom code.

## Architecture gotchas

- **Stock mutations happen only in `estoque/signals.py`**, not in views. Do not add stock math to views.
- `estoque_disponivel` is a computed `@property` (`estoque_atual - estoque_reservado`) — not stored in DB.
- Signal handlers use `select_for_update()` + `transaction.atomic()` to prevent race conditions — do not remove.
- Order status flow: `SOLICITADO → RESERVADO → EMPENHADO → ENTREGUE` (or `CANCELADO`). Stock cannot be decremented until an empenho PDF is attached.
- Views are a package (`estoque/views/`), one file per entity; shared utilities live in `_base.py`.

## Settings

- `DATABASE_URL` absent → SQLite (local). Docker injects it → PostgreSQL 17.
- Two UI themes per user (`classic`/`modern`) via `PerfilUsuario.tema_ui`; injected into all templates by `estoque.context_processors.tema_ui_context`.

## Skills disponíveis (`.opencode/skills/`)

Use o tool `skill` para carregar uma skill quando a tarefa se encaixar:

| Skill                 | Quando usar           |
|-----------------------|-----------------------|
| `coding-guidelines`   | Ao escrever, modificar ou revisar código — implementação, refatoração, bug fixes, features. **Não** usar para design de arquitetura ou documentação. |
| `docs-writer`         | Ao criar ou editar arquivos de documentação (`.md`, READMEs, `/docs`). **Não** usar para comentários de código ou JSDoc. |
| `tlc-spec-driven`     | Planejamento de projetos e features (4 fases: Specify → Design → Tasks → Execute). Usar para iniciar projetos, mapear codebase, especificar features, implementar com commits atômicos, rastrear decisões entre sessões. Gatilhos: "initialize project", "map codebase", "specify feature", "implement", "quick fix", "pause/resume work". |

## Canonical docs

Before making significant changes, consult `.specs/`:
- `.specs/codebase/` — architecture, conventions, concerns
- `.specs/project/STATE.md` — current project state and active work
- `.specs/project/ROADMAP.md` — planned features
