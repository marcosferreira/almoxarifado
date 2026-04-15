# Use a multi-stage build to keep the final image small
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy the project files
COPY pyproject.toml uv.lock ./

# Install the project's dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Final stage
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy the environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Add the virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Copy the rest of the application code
COPY . .

# Create directory for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Run collectstatic
# Note: SECRET_KEY is required for collectstatic if it's used in settings
# We provide a dummy one for the build process if not present.
RUN SECRET_KEY=dummy-key-for-collectstatic python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Entry point to run migrations and start the server
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
