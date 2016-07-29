from django.test import TestCase
from rest_framework.test import APITestCase

from accounts.models import User
from accounts.tests import create_users
from accounts.consts import UserType, BureauType

from functools import partial

from unittest.mock import MagicMock


create_user1 = partial(User.objects.create_user,
                       username='user1',
                       nickname='user1',
                       password='user1')


class UserCreationTestCase(TestCase):

    def test_create_government(self):
        user = create_user1(user_type=UserType.government)

        self.assertEqual(user.bureau_type, BureauType.none)
        self.assertIsNone(user.user_data)

    def test_create_company(self):
        user = create_user1(user_type=UserType.company)

        self.assertIsNotNone(user.user_data)

    def test_create_bureau(self):
        user = create_user1(user_type=UserType.bureau,
                            bureau_type=BureauType.media)

        self.assertEqual(user.bureau_type, BureauType.media)


class ReportsAPITestCase(APITestCase):

    def setUp(self):
        self.user, self.gov = create_users()

    def test_company_has_change_reports_perm(self):
        self.client.force_authenticate(self.user)

        res = self.client.get('/api/users/%d/' % self.user.id)
        self.assertTrue(res.data['user_data']['perms']['change'])

    def test_confict(self):
        user = User.objects.create_user(
            username='123',
            nickname='123',
            password='123'
        )

        from qiniu import BucketManager
        BucketManager.stat = MagicMock(return_value=[{'mimeType': 'fuck'}])
        self.client.force_authenticate(self.user)

        res = self.client.post(
            '/api/users/{0}/reports/'.format(self.user.id), {
                'path': '1/1.txt'
            }, format='json'
        )

        self.assertEqual(res.status_code, 201)

        self.client.force_authenticate(user)

        res = self.client.get('/api/users/{0}/reports/'.format(user.id))

        self.assertEqual(len(res.data['results']), 0)

    def test_create_delete(self):
        from qiniu import BucketManager
        BucketManager.stat = MagicMock(return_value=[{'mimeType': 'fuck'}])
        self.client.force_authenticate(self.user)

        res = self.client.post(
            '/api/users/{0}/reports/'.format(self.user.id), {
                'path': '1/1.txt'
            }, format='json'
        )

        self.assertEqual(len(self.user.user_data.reports.all()), 1)
        id = res.data['id']

        self.client.delete(
            '/api/users/{0}/reports/{1}/'.format(self.user.id, id)
        )

        self.assertEqual(len(self.user.user_data.reports.all()), 0)


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', nickname='user1', password='user1',
            id=1,
            user_type=UserType.company)
        self.gov = User.objects.create_user(
            username='user2', nickname='user2', password='user1',
            id=2,
            user_type=UserType.government)

    def test_login_with_wrong_password(self):
        res = self.client.post(
            '/api/users/login/',
            {
                'username': 'user1',
                'password': 'user',
            }, format='json'
        )

        self.assertEqual(res.status_code, 400)

    def test_login(self):
        res = self.client.post(
            '/api/users/login/',
            {
                'username': 'user1',
                'password': 'user1',
            }, format='json'
        )

        self.assertEqual(res.status_code, 200)

    def test_get_my_data(self):
        self.client.force_authenticate(self.user)
        res = self.client.get('/api/users/me/')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['username'], 'user1')

    def test_logout_and_cannot_request_me(self):
        self.client.login(username='user1', password='user1')

        res = self.client.get('/api/users/logout/')

        self.assertEqual(res.status_code, 200)

        res = self.client.get('/api/users/me/')
        self.assertEqual(res.status_code, 404)

    def test_get_user(self):
        res = self.client.get('/api/users/1/')

        self.assertDictContainsSubset({
            'id': 1,
            'nickname': 'user1',
            'username': 'user1',
            'user_type': UserType.company.value,
            'bureau_type': BureauType.none.value,
            'url': '/users/1/'
        }, res.data)

    def test_anonymouse_get_user_data(self):
        res = self.client.get('/api/users/1/')
        self.assertNotIn('user_data', res.data)

    def test_my_user_data(self):
        self.client.force_authenticate(self.user)
        res = self.client.get('/api/users/1/')
        self.assertIn('user_data', res.data)

    def test_patch_my_user_data(self):
        self.client.force_authenticate(self.user)
        res = self.client.patch('/api/users/me/userdata/', {
            'name': 'cowboy',
        }, format='json')

        self.assertEqual(res.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.user_data.name, 'cowboy')

    def test_patch_others_user_data(self):
        self.client.force_authenticate(self.user)
        res = self.client.patch('/api/users/2/userdata/', {
            'name': 'cowboy',
        }, format='json')

        self.assertEqual(res.status_code, 404)

    def test_government_patches_others_user_data(self):
        self.client.force_authenticate(self.gov)
        res = self.client.patch('/api/users/1/userdata/', {
            'name': 'gay',
        }, format='json')

        self.assertEqual(res.status_code, 200)

        self.user.user_data.refresh_from_db()
        self.assertEqual(self.user.user_data.name, 'gay')
