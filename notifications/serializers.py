from rest_framework import serializers
from rest_framework.reverse import reverse

from enhancements.rest import registry

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    message = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'created_time', 'message', 'has_read', 'module')

    def get_message(self, instance):
        return instance.message

registry.register(Notification, NotificationSerializer)
