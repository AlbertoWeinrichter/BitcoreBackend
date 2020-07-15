from configurations import Configuration, values

from .base import Base


class Production(Base, Configuration):
    BITCORE_SERVER_TYPE = "pro"
    DEBUG = values.BooleanValue(True)
    BASE_DIR = Base.BASE_DIR
    SECRET_KEY = values.SecretValue()

    ALLOWED_HOSTS = [
        "127.0.0.1",
        "0.0.0.0",
        "localhost",
        "nuxtstaging.bitcoregaming.local",
        "nuxt.bitcoregaming.local",
        "nuxt.bitcoregaming.com",
        "bitcoregaming.com",
        "backend"
    ]

    # WEBSOCKETS - DJANGO CHANNELS
    ASGI_APPLICATION = "config.routing.application"
    CHANNEL_LAYERS = {
        'default': {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("redis", 6379)],
            },
        }
    }

    # HAYSTACK CONFIGURATION
    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
            'URL': 'http://elasticsearch:9200/',
            'INDEX_NAME': 'haystack',
        },
    }
