#!/bin/sh
set -e

npm run build

python manage.py migrate --noinput

python manage.py collectstatic --noinput

exec gunicorn apda.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 150
