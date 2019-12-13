# Configuration template
# Rename to settings_private.py

"""
Copyright (c) 2019 Gabriel Kind
Hochschule Mittweida, University of Applied Sciences

Released under the MIT license
"""

import os

ROOT_URL = 'http://localhost:8000'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

ADMINS = (
    #('Max Mustermann', 'doe@example.com'),
)

# URL prefix and file system root for static files.
# If loading static files fails try prepending ROOT_URL
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'example.com',
        'PORT': '5432',
    }
}

# Host Header values allowed to access the site when DEBUG is False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Mail settings
SERVER_EMAIL = "cyanofactory@example.com"
DEFAULT_FROM_EMAIL = "cyanofactory@localhost"
EMAIL_HOST = 'mail.example.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
EMAIL_USE_SSL = True

