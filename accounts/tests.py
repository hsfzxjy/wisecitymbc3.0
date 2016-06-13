from django.test import TestCase
from rest_framework.test import APITestCase

from .models import User

from .consts import UserType, BureauType


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

    def test_get(self):
        res = self.client.get('/api/users/1/')

        self.assertEqual(res.data, {
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
