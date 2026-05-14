#!/bin/bash

# Exit on any error
set -e

# Collect static files for current code version
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Wait for database to be reachable (retry loop)
echo "Waiting for database..."
RETRIES=30
until python -c "
import socket, os

db_url = os.environ.get('DATABASE_URL', '')
if not db_url:
    raise SystemExit('DATABASE_URL not set')

# Parse host and port from DATABASE_URL
# Format: postgres://user:pass@host:port/dbname
rest = db_url.split('@')[1] if '@' in db_url else db_url
host = rest.split(':')[0] if ':' in rest else rest.split('/')[0] if '/' in rest else rest
port_part = rest.split(':')[1] if rest.count(':') >= 1 else '5432'
port = int(port_part.split('/')[0]) if '/' in port_part else int(port_part)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)
result = sock.connect_ex((host, port))
sock.close()
if result != 0:
    raise SystemExit(f'Cannot connect to {host}:{port} (error code {result})')
print(f'Connected to {host}:{port}')
" 2>&1; do
    RETRIES=$((RETRIES - 1))
    if [ $RETRIES -le 0 ]; then
        echo "Database not available after 30 attempts, exiting."
        exit 1
    fi
    echo "Database unavailable, retrying in 2s... ($RETRIES attempts left)"
    sleep 2
done

echo "Database is ready."

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Run gunicorn
echo "Starting server..."
exec "$@"
