from unittest import SkipTest
from rest_framework.test import APITestCase

from accounts.tests import create_users

from files.consts import FileType
from files import utils

from urllib.request import urlopen

import os.path


def make_path(file_name):
    return os.path.join(os.path.dirname(__file__), 'test_files', file_name)


class FileTestCase(APITestCase):

    INSTALLED_APPS = [
        'enhancements.rest.apps.AutoDiscoverConfig',
        'rules.apps.AutodiscoverRulesConfig',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'accounts',
        'files',
    ]

    def setUp(self):
        raise SkipTest
        self.user, self.gov = create_users()
        self.client.force_authenticate(self.user)

    def test_create_txt(self):
        key = utils.upload_file(make_path('testfile.txt'))
        res = self.client.post('/api/files/', {
            'path': key
        }, format='json')

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['file_name'], 'testfile.txt')
        self.assertEqual(res.data['file_type'], FileType.file)

    def test_create_image(self):
        key = utils.upload_file(make_path('testimage.jpg'))
        res = self.client.post('/api/files/', {
            'path': key
        }, format='json')

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['file_name'], 'testimage.jpg')
        self.assertEqual(res.data['file_type'], FileType.image)

    def test_create_video(self):
        key = utils.upload_file(make_path('movie.ogg'))
        res = self.client.post('/api/files/', {
            'path': key
        }, format='json')

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['file_name'], 'movie.ogg')
        self.assertEqual(res.data['file_type'], FileType.video)


class FileRetrieveTestCase(APITestCase):

    INSTALLED_APPS = [
        'enhancements.rest.apps.AutoDiscoverConfig',
        'rules.apps.AutodiscoverRulesConfig',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'accounts',
        'files',
    ]

    def setUp(self):
        raise SkipTest
        self.user, self.gov = create_users()
        self.client.force_authenticate(self.user)

    def test_download(self):
        self.key = utils.upload_file(make_path('testfile.txt'))

        res = self.client.post('/api/files/', {
            'path': self.key
        }, format='json')

        self.assertEqual(res.status_code, 201)

        fid = res.data['id']
        content = urlopen(res.data['storage_url']).read()
        self.assertEqual(content, b'Test\n')

        res = self.client.delete('/api/files/%s/' % fid)

        self.assertEqual(res.status_code, 204)


class FileDeleteTestCase(APITestCase):

    INSTALLED_APPS = [
        'enhancements.rest.apps.AutoDiscoverConfig',
        'rules.apps.AutodiscoverRulesConfig',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'accounts',
        'files',
    ]

    def setUp(self):
        self.user, self.gov = create_users()
        self.client.force_authenticate(self.user)
        self.key = utils.upload_file(make_path('testfile.txt'))

    def test_delete(self):
        res = self.client.post('/api/files/', {
            'path': self.key
        }, format='json')

        self.assertEqual(res.status_code, 201)

        res = self.client.delete('/api/files/%s/' % res.data['id'])

        self.assertEqual(res.status_code, 204)
