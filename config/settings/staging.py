from configurations import Configuration, values

from .base import Base


class Staging(Base, Configuration):
    BITCORE_SERVER_TYPE = "sta"
    DEBUG = values.BooleanValue(True)
    BASE_DIR = Base.BASE_DIR
    SECRET_KEY = values.SecretValue()

    ALLOWED_HOSTS = [
        "127.0.0.1",
        "0.0.0.0",
        "localhost",
        "nuxtstaging.bitcoregaming.local",
        "nuxtstaging.bitcoregaming.com",
        "staging.bitcoregaming.com",
        "backendstaging"
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
