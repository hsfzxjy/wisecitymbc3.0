from wisecitymbc.settings import *

INSTALLED_APPS = [
    'enhancements.rest.apps.AutoDiscoverConfig',
    'enhancements.rest.tests',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'accounts',
    'files'
]

SECRET_KEY = 'fuck'

ROOT_URLCONF = 'enhancements.rest.tests.urls'
