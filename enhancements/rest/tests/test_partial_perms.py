from django.test import override_settings

from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User
from accounts.consts import UserType

from .models import Goods


class PartialPermsTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username='user1', password='user1user',
            nickname='user1',
            user_type=UserType.government)
        self.user2 = User.objects.create(
            username='user2', password='usersgsagdsg',
            nickname='user2',
            user_type=UserType.company)
        self.goods = Goods.objects.create(id=1, name='goods1', price=2)
        self.goods2 = Goods.objects.create(id=2, name='goods2', price=3)

    def test_get(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get('/goods/1/')

        self.assertEqual(response.data, {
            'id': 1,
            'name': 'goods1'
        })

    def test_patch(self):
        self.client.force_authenticate(self.user2)
        response = self.client.patch('/goods/2/',
                                     dict(name='newname'),
                                     format='json'
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': 2,
            'name': 'newname',
        })
