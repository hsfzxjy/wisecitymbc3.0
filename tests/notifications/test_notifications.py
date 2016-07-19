from django.test import SimpleTestCase, TestCase
from rest_framework.test import APITestCase

from notifications import formatter

from notifications import dispatch

from notifications import registry
registry.register('greet')


class ViewTestCase(APITestCase):

    INSTALLED_APPS = [
        'enhancements.rest.apps.AutoDiscoverConfig',
        'rules.apps.AutodiscoverRulesConfig',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'accounts',
        'files',
        'notifications',
    ]

    def setUp(self):
        from accounts.tests import create_users

        self.user, self.gov = create_users()

        self.n = dispatch.send(
            user=self.user,
            template="Fuck you! {{user.nickname}}",
            url='/api/n/',
            module="greet",
        )

    def test_filter(self):
        registry.register('greet2')
        self.n2 = dispatch.send(
            user=self.user,
            template="Fuck you! {{user.nickname}}",
            url='/',
            module="greet2",
        )

        self.client.force_authenticate(self.user)
        res = self.client.get('/api/n/?module=greet')
        self.assertEqual(len(res.data['results']), 1)
        res = self.client.get('/api/n/?has_read=True')
        self.assertEqual(len(res.data['results']), 0)

    def test_mark(self):
        self.n2 = dispatch.send(
            user=self.user,
            template="Fuck you! {{user.nickname}}",
            url='/',
            module="greet",
        )

        self.client.force_authenticate(self.user)
        res = self.client.get(
            '/api/n/mark_as_read/?ids=%s' %
            ','.join(map(str, (self.n.id, self.n2.id)))
        )
        self.assertEqual(res.status_code, 200)

        self.client.force_authenticate(self.user)
        res = self.client.get(
            '/api/n/mark_as_read/?ids=a,%s' %
            ','.join(map(str, (self.n.id, self.n2.id)))
        )
        self.assertEqual(res.status_code, 400)

        res = self.client.get('/api/n/', follow=True)
        self.assertTrue(res.data['results'][0]['has_read'])

    def test_list(self):
        res = self.client.get('/api/n/')
        self.assertEqual(res.status_code, 404)

        self.client.force_authenticate(self.user)
        res = self.client.get('/api/n/')

        self.assertEqual(res.status_code, 200)
        self.assertDictContainsSubset(
            {
                'message': "Fuck you! company",
                "has_read": False,
            },
            res.data['results'][0]
        )

        self.client.force_authenticate(self.gov)
        res = self.client.get('/api/n/')
        self.assertListEqual(res.data['results'], [])


class FormatterTestCase(SimpleTestCase):

    INSTALLED_APPS = [
        'enhancements.rest.apps.AutoDiscoverConfig',
        'rules.apps.AutodiscoverRulesConfig',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'accounts',
        'files',
        'notifications',
    ]

    def test_variables(self):
        tmpl = """{{ user['name'] }}{{ 12 }}"""
        varialbes = formatter.extract_variables(tmpl, user={
            'name': 'hsfzxjy'
        })

        self.assertEqual(varialbes, {
            """ user['name'] """: 'hsfzxjy',
            """ 12 """: '12'
        })

        str = formatter.render(tmpl, varialbes)

        self.assertEqual(str, "hsfzxjy12")


class DispatchTestCase(TestCase):

    def setUp(self):
        from accounts.models import User

        self.user = User.objects.create_user(
            username='admin', password='admin', nickname='admin')

    def test_dispatch(self):
        dispatch.send(
            user=self.user,
            template='Hi! {{user.nickname}}.',
            url='/',
            module='greet'
        )
        self.assertEqual(
            self.user.notifications.all()[0].message,
            'Hi! admin.'
        )

    def test_sender(self):
        sender = dispatch.Sender(user=self.user)
        sender.pack(template='Hi! {{user.nickname}}{{text}}', url='/')\
            .pack(module='greet')\
            .send(text='fuck')

        self.assertEqual(
            self.user.notifications.all()[0].message,
            'Hi! adminfuck'
        )


class RegistryTestCase(TestCase):

    def test_register(self):
        from notifications import registry

        registry.register('mod1')
        self.assertTrue(registry.has_module('mod1'))

        registry.register('mod1')

        try:
            registry.register('mod1', silent=False)
        except Exception as e:
            self.assertTrue('registered' in e.args[0])

    def test_unregister(self):
        from notifications import registry

        registry.register('mod1')
        self.assertTrue(registry.has_module('mod1'))

        registry.unregister('mod1')

        self.assertFalse(registry.has_module('mod1'))
