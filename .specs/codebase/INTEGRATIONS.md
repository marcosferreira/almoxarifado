# External Integrations

## Infrastructure

### PostgreSQL 17

**Service:** PostgreSQL 17 (via `postgres:17-alpine` Docker image)
**Purpose:** Primary data store
**Implementation:** Django ORM with psycopg 3 binary driver
**Configuration:** `DATABASE_URL` environment variable, defaults to SQLite if not set
**Authentication:** Username/password via environment variables

### Nginx

**Service:** nginx:alpine
**Purpose:** Reverse proxy, static/media file serving with caching
**Configuration:** `nginx/default.conf` — upstream django on `app:8000`, 100M client max body size, 30d cache for static/media

## External APIs

**None.** The system has no external API integrations. No webhooks, no third-party API clients.

## Email / Notifications

**None.** No email backend configured, no notification system.

## File Storage

**Backend:** Django `FileSystemStorage` (local filesystem)
**Upload location:** `media/empenhos/` for empenho PDF attachments
**Serving:** Via nginx in production, Django `static()` in development

## Background Jobs

**None.** All stock mutations happen synchronously in request-response cycle via Django signals. No task queue (Celery, RQ, etc.)
