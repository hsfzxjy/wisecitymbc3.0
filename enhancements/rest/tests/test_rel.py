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

        Goods.objects.create(name='g2', price=2, id=2)

        response = self.client.patch('/buckets/1/',
                                     {'goods': [1, 2, 3]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': 1,
            'name': 'b',
            'goods': [{
                'id': 1,
                'name': 'g1'
            }, {
                'id': 2,
                'name': 'g2'
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

    def test_post(self):
        response = self.client.post(
            '/boxes/1/balls/', {'box': 1}, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['box']['id'], 1)

    def test_list(self):
        res = self.client.get('/boxes/')

        self.assertEqual(res.status_code, 200)

    def test_patch(self):
        id = Ball.objects.all()[0].id
        Box.objects.create(id=2)

        response = self.client.patch(
            '/boxes/1/balls/%d/' % id, {'box': 2}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['box']['id'], 2)
