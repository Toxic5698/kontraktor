#?/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

export DJANGO_SUPERUSER_EMAIL=petr@cechpetr.cz
export DJANGO_SUPERUSER_USERNAME=petr
export DJANGO_SUPERUSER_PASSWORD=a2345
python manage.py createsuperuser --noinput --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --password $DJANGO_SUPERUSER_PASSWORD

gunicorn kontraktor.wsgi:application --bind 0.0.0.0:8000 --workers 2
