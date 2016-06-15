from django.test import TestCase

from .html import standardize


class HTMLTestCase(TestCase):

    INSTALLED_APPS = []

    def test_standardize(self):
        html = '<b>12<script>3</script>'

        self.assertEqual(standardize(html), '<b>12</b>')
