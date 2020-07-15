import os

import django
from channels.routing import get_default_application
from configurations import importer  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")

importer.install()

django.setup()
channels_application = get_default_application()
