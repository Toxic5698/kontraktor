#?/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

export DJANGO_SUPERUSER_EMAIL=petr@cechpetr.cz
export DJANGO_SUPERUSER_USERNAME=petr
export DJANGO_SUPERUSER_PASSWORD=12345
DJANGO_SUPERUSER_PASSWORD=12345 python manage.py createsuperuser --no-input --username=petr  --email=petr@cechpetr.cz
gunicorn kontraktor.wsgi:application --bind 0.0.0.0:8000 --workers 2
