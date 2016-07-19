from rest_framework.test import APITestCase

from finance.models import Stock


class FinanceTestCase(APITestCase):

    def setUp(self):
        self.stocks = []

        for i in range(20):
            stock = Stock.objects.create(
                name='stock %s' % i,
                price=12.00,
                volume=12.00,
                company_info='company %s' % i,
            )

            stock.price = 13.00
            stock.save()

            self.stocks.append(stock)

        self.test_stock = self.stocks[0]

    def test_log_count(self):
        res = self.client.get('/api/stocks/%s/logs/' % self.test_stock.id)

        self.assertEqual(len(res.data['results']), 2)
