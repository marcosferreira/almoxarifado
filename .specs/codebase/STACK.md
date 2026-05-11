# Tech Stack

**Analyzed:** 2026-05-11

## Core

- Framework: Django 6.0.4
- Language: Python 3.12
- Runtime: CPython
- Package manager: uv (astral-sh)

## Frontend

- UI Framework: Django Templates (server-rendered)
- Styling: Tailwind CSS v3 (CDN), custom design-tokens CSS
- State/Interactivity: Alpine.js 3.x (CDN)
- Fonts: Plus Jakarta Sans (Google Fonts, modern theme), Segoe UI (classic theme)

## Backend

- API Style: Django views (function-based, no DRF)
- Database: PostgreSQL 17 (production), SQLite (dev fallback via DATABASE_URL)
- ORM: Django ORM
- Authentication: Django contrib.auth (session-based)

## Testing

- Unit/Integration: `django.test.TestCase` (Django's built-in test framework)

## Infrastructure

- Containerization: Docker multi-stage build (uv builder → python:3.12-slim)
- Orchestration: docker-compose (app + nginx + postgres)
- Reverse Proxy: nginx:alpine (static/media serving + proxy pass)
- Static Files: WhiteNoise (CompressedManifestStaticFilesStorage)
- Database Driver: psycopg 3 (binary)
- WSGI Server: Gunicorn

## External Services

- None currently integrated beyond the database

## Development Tools

- Environment: python-dotenv
- Docker compose for local dev
