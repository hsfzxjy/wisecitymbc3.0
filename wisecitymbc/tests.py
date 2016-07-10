from django.test import TestCase


class TimeZoneTestCase(TestCase):

    def test_timezone(self):
        from django.utils import timezone
        from datetime import datetime

        self.assertEqual(timezone.now().hour, datetime.now().hour)
