from django.test import SimpleTestCase, TestCase

from . import formatter

from . import dispatch

from . import registry
registry.register('greet')


class FormatterTestCase(SimpleTestCase):

    available_apps = ['notifiactions']

    def test_variables(self):
        tmpl = """{{ user['name'] }}{{ 12 }}"""
        varialbes = formatter.extract_variables(tmpl, user={
            'name': 'hsfzxjy'
        })

        self.assertEqual(varialbes, {
            """ user['name'] """: 'hsfzxjy',
            """ 12 """: 12
        })

        str = formatter.render(tmpl, varialbes)

        self.assertEqual(str, "hsfzxjy12")


class DispatchTestCase(TestCase):

    def setUp(self):
        from accounts.models import User

        self.user = User.objects.create_user(
            username='admin', password='admin', nickname='admin')

    def test_dispatch(self):
        dispatch.send(self.user, 'Hi! {{user.nickname}}.', '/', 'greet')
        self.assertEqual(
            self.user.notification_set.all()[0].message,
            'Hi! admin.'
        )

    def test_sender(self):
        sender = dispatch.Sender(self.user)
        sender.pack('Hi! {{user.nickname}}{{text}}', '/')\
            .pack('greet')\
            .send(text='fuck')

        self.assertEqual(
            self.user.notification_set.all()[0].message,
            'Hi! adminfuck'
        )


class RegistryTestCase(TestCase):

    def test_register(self):
        from . import registry

        registry.register('mod1')
        self.assertTrue(registry.has_module('mod1'))

        registry.register('mod1')

        try:
            registry.register('mod1', silent=False)
        except Exception as e:
            self.assertTrue('registered' in e.args[0])

    def test_unregister(self):
        from . import registry

        registry.register('mod1')
        self.assertTrue(registry.has_module('mod1'))

        registry.unregister('mod1')

        self.assertFalse(registry.has_module('mod1'))

    def test_modules(self):
        from . import registry

        registry.register('mod1')
        registry.register('mod2')

        self.assertEqual(registry.get_modules(), ('greet', 'mod1', 'mod2'))
