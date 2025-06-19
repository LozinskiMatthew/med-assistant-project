#!/bin/sh
set -e

/app/wait_for_database.sh "$POSTGRES_HOST" "$POSTGRES_PORT"

echo "Making migrations..."
python manage.py makemigrations --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
