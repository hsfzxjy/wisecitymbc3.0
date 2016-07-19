# coding=utf-8

from rest_framework.test import APITestCase

from accounts.tests import create_users
from articles.models import Article

from articles.consts import ArticleType

from unittest.mock import MagicMock
from qiniu import BucketManager
BucketManager.stat = MagicMock(return_value=[{'mimeType': 'fuck'}])


class AttachmentsTestCase(APITestCase):

    def setUp(self):
        self.user, self.gov = create_users()

    def test_post(self):
        file_id = self.client.post(
            '/api/files/', {
                'path': '1/1.txt'
            }, format='json'
        ).data['id']

        self.client.force_authenticate(self.user)
        res = self.client.post(
            '/api/articles/',
            {
                'title': 'title',
                'content': '<b>content',
                'attachments': [file_id]
            }, format='json'
        )
        self.assertEqual(len(res.data['attachments']), 1)


class ArticleTestCase(APITestCase):

    def setUp(self):
        self.user, self.gov = create_users()

    def test_filter_(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(
            '/api/articles/',
            {
                'title': 'title',
                'content': '<b>content'
            }, format='json'
        )

        self.assertEqual(res.status_code, 201)

        res = self.client.get('/api/articles/?article_type=1')

        self.assertEqual(len(res.data['results']), 1)

    def test_post(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(
            '/api/articles/',
            {
                'title': 'title',
                'content': '<b>content'
            }, format='json'
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['content'], '<b>content</b>')
        self.assertEqual(res.data['summary'], '**content**\n')
        self.assertEqual(res.data['article_type'], ArticleType.company)

    def test_partial(self):
        self.client.force_authenticate(self.user)

        res = self.client.post(
            '/api/articles/',
            {
                'title': 'title',
                'content': '<b>content'
            }, format='json'
        )
        self.assertEqual(res.status_code, 201)

        res = self.client.get(
            '/api/articles/%s/?exclude=content' % res.data['id']
        )
        self.assertNotIn('content', res.data)

    def test_patch(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(
            '/api/articles/',
            {
                'title': 'title',
                'content': '<b>content'
            }, format='json'
        )

        res = self.client.patch(
            '/api/articles/%d/' % res.data['id'],
            {
                'title': 'Fuck'
            }, format='json'
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['title'], 'Fuck')

        self.client.logout()

        res = self.client.patch(
            '/api/articles/%d/' % res.data['id'],
            {
                'title': 'Fuck'
            }, format='json'
        )

        self.assertEqual(res.status_code, 403)

    def test_filter(self):
        for i in range(1, 20):
            Article.objects.create(
                author=self.user,
                title='我是中国人',
                content='content%s asshole' % i,
            )
        Article.objects.create(
            author=self.gov,
            title='我是中国人',
            content='contents asshole',
        )
        res = self.client.get(
            '/api/articles/?author__id={0}&limit=100'.format(self.user.id))

        self.assertEqual(len(res.data['results']), 19)

    def test_slug_fields(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(
            '/api/articles/',
            {
                'title': 'title',
                'content': '<b>content',
                'tags': ['1', '1']
            }, format='json'
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['tags'], ['1'])

    def test_url(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(
            '/api/articles/',
            {
                'title': 'title',
                'content': '<b>content',
                'tags': ['1', '1']
            }, format='json'
        )
        self.assertEqual(
            res.data['url'], '/detail/articles/{0}/'.format(res.data['id']))
