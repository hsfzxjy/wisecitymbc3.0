from django.test import SimpleTestCase
from django.conf import settings

import os

output_file_names = [os.path.join(os.path.dirname(__file__), 'a.json')]


expected_result = {
    'constants_test': {
        'TYPES': {
            'Government': 'Government',
        },
        'UserType': {
            'Gov': 1,
            'Com': 2,
            'Chr': 3
        }
    }
}


class GenerateTestCase(SimpleTestCase):

    def setUp(self):
        self._old = settings.CONSTS_OUTPUT_PATHS
        settings.CONSTS_OUTPUT_PATHS = output_file_names

    def tearDown(self):
        settings.CONSTS_OUTPUT_PATHS = self._old

    def test_collect(self):
        from enhancements.constants.core import collect_consts

        self.assertDictContainsSubset(expected_result, collect_consts())

    def test_generate(self):
        from enhancements.constants.core import generate_consts

        generate_consts()

        import json

        for path in settings.CONSTS_OUTPUT_PATHS:
            print(path)
            with open(path, 'r') as fp:
                self.assertDictContainsSubset(expected_result, json.load(fp))
