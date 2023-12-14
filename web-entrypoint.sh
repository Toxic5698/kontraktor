#?/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

DJANGO_SUPERUSER_PASSWORD=12345 python manage.py createsuperuser --no-input --username=petr  --email=petr@cechpetr.cz
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT} --workers ${WEB_CONCURRENCY}
