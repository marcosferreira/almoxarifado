#!/bin/bash

# Exit on any error
set -e

# Collect static files for current code version
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Run gunicorn
echo "Starting server..."
exec "$@"
