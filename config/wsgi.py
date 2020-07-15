import os
from configurations.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
os.environ.setdefault("DJANGO_CONFIGURATION", "Development")

application = get_wsgi_application()
