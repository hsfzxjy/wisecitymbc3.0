# coding=utf-8

from rest_framework.test import APITestCase

from accounts.tests import create_users
from .models import Article

from .consts import ArticleType


class ArticleTestCase(APITestCase):

    def setUp(self):
        self.user, self.gov = create_users()

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

    def test_search(self):
        for i in range(1, 20):
            Article.objects.create(
                author=self.user,
                title='我是中国人',
                content='content%s asshole' % i,
            )
        res = self.client.get(
            '/api/articles/search/?keyword=%E6%88%91%E6%98%AF')

        self.assertEqual(len(res.data['results']), 10)
