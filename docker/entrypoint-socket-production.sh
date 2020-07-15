python manage.py rebuild_index --noinput

daphne -b 0.0.0.0 -p 9000 config.asgi:channels_application