from rest_framework import serializers

from .models import User, UserData

from enhancements import rest


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('nickname', 'username', 'bureau_type',
                  'user_type', 'user_data')
        read_only_fields = ('user_data', )


class UserDataSerialiser(serializers.ModelSerializer):

    class Meta:
        model = UserData
        exclude = ('id',)

rest.registry.register(User, UserSerializer)
rest.registry.register(UserData, UserDataSerialiser)
