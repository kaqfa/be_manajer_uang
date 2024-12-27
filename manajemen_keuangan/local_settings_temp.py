from .settings import *

SECRET_KEY = ''
DEBUG = False
ALLOWED_HOSTS = ['*', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'NAME': 'cofast',
        'USER': 'devel',
        'PASSWORD': 'develpass',
        'HOST': 'db',
        'PORT': 3306,
        'OPTIONS': {
            'auth_plugin': 'mysql_native_password'
        }
    }
}