from django.test import SimpleTestCase

# Create your tests here.


expected_result = {
    'test_app': {
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

    available_apps = [
        'tests.test_app'
    ]

    def test_collect(self):
        from ..core import collect_consts

        self.assertEqual(expected_result, collect_consts())

    def test_generate(self):
        from ..core import generate_consts

        generate_consts()

        import json

        from django.conf import settings

        for path in settings.CONSTS_OUTPUT_PATHS:
            with open(path, 'r') as fp:
                self.assertEqual(expected_result, json.load(fp))
