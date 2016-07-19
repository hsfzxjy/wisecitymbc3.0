SECRET_KEY = 'fake'

INSTALLED_APPS = ['tests.test_app']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app_wisecitymbc',
        'USER': 'root',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}