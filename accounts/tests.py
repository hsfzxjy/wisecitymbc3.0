from django.test import TestCase
from rest_framework.test import APITestCase

from .models import User

from .consts import UserType, BureauType


def create_users():
    return User.objects.create_user(
        # id=1,
        username='company',
        nickname='company',
        password='company',
        user_type=UserType.company,
    ), User.objects.create_user(
        # id=2,
        username='gov',
        nickname='gov',
        password='goverment',
        user_type=UserType.government
    )


class UserTestCase(TestCase):

    INSTALLED_APPS = [
        'enhancements.rest.apps.AutoDiscoverConfig',
        'rules.apps.AutodiscoverRulesConfig',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'accounts',
        'files'
    ]

    def test_create_gov(self):
        user = User.objects.create_user(
            username='user1', nickname='user1', password='user1',
            user_type=UserType.government,
            bureau_type=BureauType.media)

        self.assertEqual(user.bureau_type, BureauType.none)
        self.assertIsNone(user.user_data)

    def test_create_com(self):
        user = User.objects.create_user(
            username='user1', nickname='user1', password='user1',
            user_type=UserType.company,
            bureau_type=BureauType.media)

        self.assertIsNotNone(user.user_data)

    def test_create_bureau(self):
        user = User.objects.create_user(
            username='user1', nickname='user1', password='user1',
            user_type=UserType.bureau,
            bureau_type=BureauType.media)

        self.assertEqual(user.bureau_type, BureauType.media)


class UserRulesTestCase(TestCase):

    def test_rules(self):
        import rules

        rules.remove_perm('accounts.add_user')
        rules.add_perm('accounts.add_user', rules.always_allow)

        user = User.objects.create_user(
            username='user1', nickname='user1', password='user1',
            user_type=UserType.government,
            bureau_type=BureauType.media)

        self.assertTrue(user.has_perm('accounts.add_user'))


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', nickname='user1', password='user1',
            id=1,
            user_type=UserType.company,
            bureau_type=BureauType.media)
        self.gov = User.objects.create_user(
            username='user2', nickname='user2', password='user1',
            id=2,
            user_type=UserType.government,
            bureau_type=BureauType.media)

    def test_get(self):
        res = self.client.get('/api/users/1/')

        self.assertEqual(res.data, {
            'id': 1,
            'nickname': 'user1',
            'username': 'user1',
            'user_type': UserType.company.value,
            'bureau_type': BureauType.none.value,
        })

        res = self.client.get('/api/users/2/')

        self.assertEqual(res.data, {
            'id': 2,
            'nickname': 'user2',
            'username': 'user2',
            'user_type': UserType.government.value,
            'bureau_type': BureauType.none.value,
        })

        self.client.force_authenticate(self.gov)

        res = self.client.get('/api/users/1/')

        self.assertEqual(res.data, {
            'id': 1,
            'nickname': 'user1',
            'username': 'user1',
            'user_type': UserType.company.value,
            'bureau_type': BureauType.none.value,
            'user_data': {
                'name': '',
                'industry': '',
                'sector': '',
                'description': '',
                'reports': []
            }
        })

        self.client.force_authenticate(self.user)

        res = self.client.get('/api/users/1/')

        self.assertEqual(res.data, {
            'id': 1,
            'nickname': 'user1',
            'username': 'user1',
            'user_type': UserType.company.value,
            'bureau_type': BureauType.none.value,
            'user_data': {
                'name': '',
                'industry': '',
                'sector': '',
                'description': '',
                'reports': []
            }
        })

        res = self.client.get('/api/users/me/')
        self.assertEqual(res.data['id'], 1)

    def test_get_user_data(self):
        # from enhancements.debug.urls import print_urls
        # print_urls()
        self.client.force_authenticate(self.user)
        res = self.client.patch('/api/users/me/userdata/', {
            'name': 'cowboy',
        }, format='json')

        # print(res.data)
        self.assertEqual(res.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.user_data.name, 'cowboy')

        res = self.client.patch('/api/users/2/userdata/', {
            'name': 'cowboy',
        }, format='json')

        self.assertEqual(res.status_code, 404)

        self.client.force_authenticate(self.gov)
        res = self.client.patch('/api/users/1/userdata/', {
            'name': 'gay',
        }, format='json')

        # print(res.data)
        self.assertEqual(res.status_code, 200)

        self.user.user_data.refresh_from_db()
        self.assertEqual(self.user.user_data.name, 'gay')
