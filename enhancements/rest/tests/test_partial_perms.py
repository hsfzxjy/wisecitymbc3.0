from django.test import TestCase, override_settings

from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.models import User
from accounts.consts import UserType


class PartialPermsTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create(
            username='user1', password='user1user', user_type=UserType.government.value)
        self.user2 = User.objects.create(
            username='user2', password='usersgsagdsg', user_type=UserType.player.value)
