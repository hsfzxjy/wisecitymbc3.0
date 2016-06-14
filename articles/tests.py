from rest_framework.test import APITestCase

from accounts.tests import create_users
from .models import Article

from .consts import ArticleType


class ArticleTestCase(APITestCase):

    INSTALLED_APPS = [
        'enhancements.rest.apps.AutoDiscoverConfig',
        'rules.apps.AutodiscoverRulesConfig',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'accounts',
        'files',
        'articles'
    ]

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
        self.assertEqual(res.data['article_type'], ArticleType.company)

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
        from watson import search as watson

        for i in range(1, 20):
            Article(
                author=self.user,
                title='title%s' % i,
                content='content%s' % i,
            ).save()
        print(list(watson.search('on')))
        res = self.client.get('/api/articles/search/?keyword=conte')

        print(res.data)
