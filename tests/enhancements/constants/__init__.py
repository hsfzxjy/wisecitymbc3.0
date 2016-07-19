from django.apps import AppConfig


class TestAppConfig(AppConfig):

    label = 'constants_test'
    name = 'tests.enhancements.constants'

default_app_config = 'tests.enhancements.constants.TestAppConfig'
