from django.test import TestCase


class CreateModelTestCase(TestCase):

    available_apps = ['tests.test_app']

    def test_create(self):
        from tests.test_app.models import Stock, StockLog

        stock = Stock.objects.create(price=1.5)

        self.assertEqual(stock.has_changed(), False)

        self.assertEqual(StockLog.objects.count(), 1, "First")

        stock.save()

        self.assertEqual(StockLog.objects.count(), 1, "Second")

        stock.price = 1.6
        stock.save()

        self.assertEqual(StockLog.objects.count(), 2, "Third")

        logs = StockLog.objects.all()

        self.assertEqual(logs[0].price, 1.5)
        self.assertEqual(logs[1].price, 1.6)

    def test_undo(self):
        from tests.test_app.models import Stock, StockLog

        stock = Stock.objects.create(price=1.5)

        stock.price = 1.6
        stock.save()

        self.assertEqual(StockLog.objects.count(), 2)

        stock.price = 1.7
        stock.save()
        self.assertEqual(StockLog.objects.count(), 3)

        stock.undo()

        self.assertEqual(stock.price, 1.6)
        self.assertEqual(Stock.objects.count(), 1)
        self.assertEqual(StockLog.objects.count(), 2)
        self.assertEqual(stock.current_log.price, 1.6)

        stock.undo()

        self.assertEqual(stock.price, 1.5)
        self.assertEqual(StockLog.objects.count(), 1)
        self.assertEqual(stock.current_log.price, 1.5)

        stock.undo()

        self.assertEqual(stock.price, 1.5)
        self.assertEqual(StockLog.objects.count(), 1)
        self.assertEqual(stock.current_log.price, 1.5)
