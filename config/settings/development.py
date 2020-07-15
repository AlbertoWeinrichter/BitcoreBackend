from configurations import Configuration, values

from .base import Base


class Development(Base, Configuration):
    BITCORE_SERVER_TYPE = "pro"
    DEBUG = values.BooleanValue(True)
    BASE_DIR = Base.BASE_DIR
    SECRET_KEY = values.SecretValue()

    ALLOWED_HOSTS = [
        "127.0.0.1",
        "localhost",
        "0.0.0.0",
        "bitcoregaming.local"
    ]

    # WEBSOCKETS - DJANGO CHANNELS
    ASGI_APPLICATION = "config.routing.application"
    CHANNEL_LAYERS = {
        'default': {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        }
    }

    # HAYSTACK CONFIGURATION
    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }

    # TODO: REMOVE THIS
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': "bitcore",
    #         'USER': "bitcore_admin",
    #         'PASSWORD': "Ikkitousen!2019",
    #         'HOST': "0.0.0.0",
    #         'PORT': 5432
    #     }
    # }
