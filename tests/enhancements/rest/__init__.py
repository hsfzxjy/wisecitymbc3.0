from django.apps import AppConfig


class RestTestAppConfig(AppConfig):

    label = 'rest_test'
    name = 'tests.enhancements.rest'

default_app_config = 'tests.enhancements.rest.RestTestAppConfig'
