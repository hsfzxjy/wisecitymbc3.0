from .models import Reply, Topic

from rest_framework import serializers

from enhancements.rest import registry


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        extra_kwargs = {
            'asker': {
                'fields': ('username', 'nickname', 'id')
            }
        }


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        extra_kwargs = {
            'author': {
                'fields': ('username', 'nickname', 'id')
            },
            'topic': {
                'fields': ('id', 'title')
            }
        }

registry.register(Topic, TopicSerializer)
registry.register(Reply, ReplySerializer)
