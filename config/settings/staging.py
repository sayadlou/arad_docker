from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['arad-imeg.herokuapp.com','127.0.0.1']



ROOT_URLCONF = 'config.urls.staging'

