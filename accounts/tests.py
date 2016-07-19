from accounts.models import User

from accounts.consts import UserType


def create_users():
    return User.objects.create_user(
        # id=1,
        username='company',
        nickname='company',
        password='company',
        user_type=UserType.company,
    ), User.objects.create_user(
        # id=2,
        username='gov',
        nickname='gov',
        password='goverment',
        user_type=UserType.government
    )
