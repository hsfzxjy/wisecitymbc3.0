from rest_framework.test import APITestCase

from .models import Reply, Topic

from accounts.tests import create_users


class QuestionsTestCase(APITestCase):

    INSTALLED_APPS = [
        'enhancements.rest.apps.AutoDiscoverConfig',
        'rules.apps.AutodiscoverRulesConfig',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'accounts',
        'questions',
        'files',
    ]

    def setUp(self):
        self.user, self.gov = create_users()

    def test_create_topic(self):
        res = self.client.post('/api/topics/', {
            'title': 'Hi'
        }, format='json')
        self.assertEqual(res.status_code, 403)

        self.client.force_authenticate(self.user)

        res = self.client.post('/api/topics/', {
            'title': 'Hi'
        }, format='json')

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['title'], 'Hi')
