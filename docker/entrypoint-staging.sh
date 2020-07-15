python manage.py rebuild_index --noinput

gunicorn config.wsgi:application --bind 0.0.0.0:8001
