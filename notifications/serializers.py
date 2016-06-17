from rest_framework import serializers
from rest_framework.reverse import reverse

from enhancements.rest import registry

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    message = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'created_time', 'message', 'url', 'has_read')

    def get_message(self, instance):
        return instance.message

    def get_url(self, instance):
        return reverse('notification-redirect', kwargs={
            'pk': instance.pk
        })

registry.register(Notification, NotificationSerializer)
