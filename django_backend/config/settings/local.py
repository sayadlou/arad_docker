from .base import *
import os
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
import socket

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('POSTGRES_DB'),
#         'USER': os.environ.get('POSTGRES_USER'),
#         'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
#         'HOST': 'postgres',
#         'PORT': '5432',
#     }
# }

ALLOWED_HOSTS = ['arad-imeg.herokuapp.com', '127.0.0.1']

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INSTALLED_APPS += [
    "debug_toolbar",
]

INTERNAL_IPS = [
    "127.0.0.1",
]
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())

INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

ROOT_URLCONF = 'config.urls.local'

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_email"

CAPTCHA_TEST_MODE = True
