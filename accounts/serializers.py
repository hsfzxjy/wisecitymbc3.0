from enhancements.rest import serializers

from .models import User, UserData


@serializers.register(User)
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('nickname', 'username', 'bureau_type',
                  'user_type', 'user_data', 'id', 'url', 'perms',
                  'is_staff')
        read_only_fields = ('user_data', )

    def get_url(self, user):
        return '/users/{0}/'.format(user.id)


@serializers.register(UserData)
class UserDataSerializer(serializers.ModelSerializer):
    pass
