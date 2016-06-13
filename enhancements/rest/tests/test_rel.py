from rest_framework.test import APITestCase
from .models import Bucket, Goods, Box, Ball


class RelTestCase(APITestCase):

    def setUp(self):
        self.bucket = Bucket.objects.create(name='b', id=1)

    def test_get(self):
        goods = self.goods = Goods.objects.create(name='g1', price=1, id=1)

        self.bucket.goods.add(goods)

        response = self.client.get('/buckets/1/')

        self.assertEqual(response.data, {
            'id': 1,
            'name': 'b',
            'goods': [{
                'id': 1,
                'name': 'g1'
            }]
        })

    def test_patch(self):
        goods = self.goods = Goods.objects.create(name='g1', price=1, id=1)

        self.bucket.goods.add(goods)

        response = self.client.patch('/buckets/1/',
                                     {'goods': [1]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': 1,
            'name': 'b',
            'goods': [{
                'id': 1,
                'name': 'g1'
            }]
        })


class NestedTestCase(APITestCase):

    def setUp(self):
        box = Box.objects.create(name='1', id=1)
        ball = Ball.objects.create(box=box)

    def test_get(self):
        response = self.client.get('/boxes/1/balls/1/')

        self.assertEqual(response.data, {
            'id': 1,
            'box': {
                'id': 1,
                'name': '1'
            }
        })
