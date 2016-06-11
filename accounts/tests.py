from django.test import TestCase

from .models import User

from .consts import UserType, BureauType


class UserTestCase(TestCase):

    def test_create_gov(self):
        user = User.objects.create_user(
            username='user1', nickname='user1', password='user1',
            user_type=UserType.government,
            bureau_type=BureauType.media)

        self.assertEqual(user.bureau_type, BureauType.none)
        self.assertIsNone(user.data)

    def test_create_com(self):
        user = User.objects.create_user(
            username='user1', nickname='user1', password='user1',
            user_type=UserType.company,
            bureau_type=BureauType.media)

        self.assertIsNotNone(user.data)

    def test_create_bureau(self):
        user = User.objects.create_user(
            username='user1', nickname='user1', password='user1',
            user_type=UserType.bureau,
            bureau_type=BureauType.media)

        self.assertEqual(user.bureau_type, BureauType.media)


class UserRulesTestCase(TestCase):

    def test_rules(self):
        import rules

        rules.remove_perm('accounts.add_user')
        rules.add_perm('accounts.add_user', rules.always_allow)

        user = User.objects.create_user(
            username='user1', nickname='user1', password='user1',
            user_type=UserType.government,
            bureau_type=BureauType.media)

        self.assertTrue(user.has_perm('accounts.add_user'))
