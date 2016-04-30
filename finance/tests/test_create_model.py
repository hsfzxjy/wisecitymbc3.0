from django.test import TestCase

class CreateModelTestCase(TestCase):

    available_apps = ['tests.test_app']

    def test_create(self):
        from tests.test_app.models import Stock, StockLog

        Stock.objects.create(price = 1.5)

        self.assertEqual(Stock.objects.get(id=1).price, 1.5)
        print(StockLog.objects.get(id=1).serialized_data)