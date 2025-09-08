from .common import *

SECRET_KEY = 'django-insecure-1_vacbfp)#7pg-#9n&u2xkp3g1#76_uclj@j49q-gbnn_9e+#j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INSTALLED_APPS += [
    'debug_toolbar',
    'silk'
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'storefront3',
        'HOST': 'postgres',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'postgres'
    }
}

CELERY_BROKER_URL = 'redis://redis:6379/1'
CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'playground.tasks.notify_customers',
        'schedule': 5,
        'args': ['Hello World!']
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        # 'TIMEOUT': 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = 'smtp4dev'
EMAIL_HOST_USER = ''
EMAIL_PASSWORD = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'from@ecommerce.com'

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: True
# }