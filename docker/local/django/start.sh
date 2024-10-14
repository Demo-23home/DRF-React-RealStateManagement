#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Wait for PostgreSQL to be available (handled by entrypoint.sh)

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --no-input

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Start the development server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
