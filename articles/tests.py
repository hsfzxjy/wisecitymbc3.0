from rest_framework.test import APITestCase

from accounts.tests import create_users

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
