from .models import Reply, Topic

from enhancements.rest import serializers


@serializers.register(Topic)
class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            'asker': {
                'fields': ('username', 'nickname', 'id')
            }
        }

    def get_url(self, topic):
        return '/detail/topics/{0}/'.format(topic.id)


@serializers.register(Reply)
class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            'author': {
                'fields': ('username', 'nickname', 'id')
            },
            'topic': {
                'fields': ('id', 'title')
            }
        }
