import json
import os

from configurations import Configuration, values
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from six.moves.urllib import request
from unipath import Path


class Base(Configuration):
    DEBUG = False
    DATABASES = values.DatabaseURLValue(os.getenv('DATABASE_URL')).setup('DATABASE_URL')  # noqa

    BASE_DIR = os.getcwd()
    PROJECT_PATH = Path(__file__).ancestor(3)
    TOP_DIR = os.path.realpath(os.path.join(BASE_DIR, os.pardir))

    SECRET_KEY = values.SecretValue().setup('SECRET_KEY')

    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    SESSION_COOKIE_AGE = 600 * 600

    INSTALLED_APPS = [
        'API.user',
        'API.comments',
        'API.votes',
        'API.publication',
        'API.releases',
        'API.notifications',
        'API.general',
        'API.patreon',
        'API.chat',
        'django_nose',
        'rest_framework',
        'rest_framework.authtoken',
        'tagulous',
        'froala_editor',
        'channels',
        'storages',
        'haystack',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    AUTH_USER_MODEL = 'user.User'

    FROALA_EDITOR_PLUGINS = (
        'align', 'char_counter', 'code_beautifier', 'code_view', 'colors', 'draggable', 'emoticons',
        'entities', 'file', 'font_family', 'font_size', 'fullscreen', 'image', 'inline_style',
        'line_breaker', 'link', 'lists', 'paragraph_format', 'paragraph_style', 'quick_insert',
        'save', 'table', 'url', 'video', 'word_paste')

    FROALA_UPLOAD_PATH = ('')
    FROALA_EDITOR_OPTIONS = {
        'key': os.getenv('FROALA_EDITOR_KEY')
    }

    include_jquery = False

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'API/froala_editor'),
    )

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'config.urls'
    WSGI_APPLICATION = 'config.wsgi.application'

    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
    ]

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    FILE_UPLOAD_PERMISSIONS = 0o644

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_HEADERS = [
        'accept',
        'accept-encoding',
        'authorization',
        'content-disposition',
        'content-type',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    ADMIN_URL = 'admin/'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'cache:11211',
        }
    }

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'API.user.bitcore_auth_backend.BitcoreTokenBackend',
        )
    }

    # EMAIL
    EMAIL_HOST = 'smtp.mailgun.org'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = True

    # S3 Storages
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = "bitcoregaming"
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    AWS_STATIC_LOCATION = 'static'
    STATIC_ROOT = BASE_DIR
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
    ADMIN_MEDIA_PREFIX = STATIC_URL

    AWS_MEDIA_LOCATION = 'media'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

    STATICFILES_LOCATION = 'static'
    MEDIAFILES_LOCATION = 'media/'
    STATICFILES_STORAGE = 'config.storage_backends.StaticStorage'
    DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'

    # This is for admin, not normal API
    AUTHENTICATION_BACKENDS = {
        'django.contrib.auth.backends.ModelBackend'
    }

    # Auth0 And JsonWebToken configuration
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
    jsonurl = request.urlopen('https://' + AUTH0_DOMAIN + '/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read().decode('utf-8'))
    cert = '-----BEGIN CERTIFICATE-----\n' + jwks['keys'][0]['x5c'][0] + '\n-----END CERTIFICATE-----'
    certificate = load_pem_x509_certificate(cert.encode('utf-8'), default_backend())
    PUBLIC_KEY = certificate.public_key()

    BOOTSTRAP_ADMIN_SIDEBAR_MENU = False
