from enhancements.rest.serializers import register, ModelSerializer

from rest_framework import serializers

from .models import Notification


@register(Notification)
class NotificationSerializer(ModelSerializer):

    message = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'created_time', 'message', 'has_read', 'module')

    def get_message(self, instance):
        return instance.message
