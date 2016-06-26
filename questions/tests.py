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

    def create_topic(self):
        return self.client.post('/api/topics/', {
            'title': 'Hi',
            'content': '<p>123'
        }, format='json')

    def login(self, user):
        self.client.force_authenticate(user)

    def test_create_topic(self):
        res = self.client.post('/api/topics/', {
            'title': 'Hi',
            'content': '<p>123'
        }, format='json')
        self.assertEqual(res.status_code, 403)

        self.client.force_authenticate(self.user)

        res = self.client.post('/api/topics/', {
            'title': 'Hi',
            'content': '<p>123'
        }, format='json')

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['title'], 'Hi')
        self.assertEqual(res.data['content'], '<p>123</p>')

    def test_patch(self):
        self.login(self.user)
        tid = self.create_topic().data['id']

        res = self.client.patch('/api/topics/%s/' % tid, {
            'content': '<b>fuck'
        }, format='json')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['content'], '<b>fuck</b>')

    def test_open_close(self):
        self.login(self.user)
        tid = self.create_topic().data['id']

        res = self.client.get('/api/topics/%s/close/' % tid)
        self.assertEqual(res.data['is_closed'], True)

        res = self.client.patch('/api/topics/%s/' % tid, {
            'content': 'b'
        }, format='json')

        self.assertEqual(res.status_code, 403)

        res = self.client.get('/api/topics/%s/open/' % tid)
        self.assertEqual(res.data['is_closed'], False)

        res = self.client.patch('/api/topics/%s/' % tid, {
            'content': 'b'
        }, format='json')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['content'], 'b')

        print(self.user.notifications.all())
        print(self.gov.notifications.all())


class ReplyTestCase(APITestCase):

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
        self.topic = Topic.objects.create(
            title='title',
            content='content',
            asker=self.user
        )

    def test_create(self):
        self.client.force_authenticate(self.user)

        res = self.client.post(
            '/api/topics/%s/replies/' % self.topic.id, {
                'content': 'reply'
            }, format='json')

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['content'], 'reply')

        self.client.force_authenticate(self.gov)

        res = self.client.post(
            '/api/topics/%s/replies/' % self.topic.id, {
                'content': 'reply'
            }, format='json')

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['content'], 'reply')

    def test_patch(self):
        self.client.force_authenticate(self.gov)

        res = self.client.post(
            '/api/topics/%s/replies/' % self.topic.id, {
                'content': 'reply'
            }, format='json')

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['content'], 'reply')

        res = self.client.patch(
            '/api/topics/%s/replies/%s/' % (self.topic.id, res.data['id']), {
                'content': 'reply'
            }, format='json')

        self.assertEqual(res.status_code, 403)

    def test_close(self):
        self.topic.close(self.user)
        self.client.force_authenticate(self.user)

        res = self.client.post(
            '/api/topics/%s/replies/' % self.topic.id, {
                'content': 'reply'
            }, format='json')

        self.assertEqual(res.status_code, 403)

        self.topic.open()

        res = self.client.post(
            '/api/topics/%s/replies/' % self.topic.id, {
                'content': 'reply'
            }, format='json')

        self.assertEqual(res.status_code, 201)

    def test_delete(self):
        self.client.force_authenticate(self.user)

        rid = self.client.post(
            '/api/topics/%s/replies/' % self.topic.id, {
                'content': 'reply'
            }, format='json').data['id']

        res = self.client.delete(
            '/api/topics/%s/replies/%s/' % (self.topic.id, rid))
        self.assertEqual(res.status_code, 204)

        res = self.client.get('/api/topics/%s/replies/' % self.topic.id)
        self.assertEqual(res.data['results'], [])
