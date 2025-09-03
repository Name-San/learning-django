from .common import *

SECRET_KEY = 'django-insecure-1_vacbfp)#7pg-#9n&u2xkp3g1#76_uclj@j49q-gbnn_9e+#j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'storefront3',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'admin123'
    }
}