from rest_framework import viewsets

from enhancements.rest.urls import register, register_nested

from .models import Reply, Topic
from accounts.consts import UserType

from django.shortcuts import get_object_or_404


@register('topics')
class TopicViewSet(viewsets.ModelViewSet):

    queryset = Topic.objects.all()

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset

        # pass when not logined
        if not user.is_authenticated():
            return qs

        if user.user_type in (UserType.government, UserType.bureau):
            return qs
        else:
            # company
            return qs.filter(asker=user)

    def create(self, *args, **kwargs):
        self.request.data['asker'] = self.request.user.id

        return super(TopicViewSet, self).create(*args, **kwargs)


@register_nested(
    'replies',
    TopicViewSet,
    'topics',
    'topic',
)
class ReplyViewSet(viewsets.ModelViewSet):

    queryset = Reply.objects.all()

    def get_queryset(self):
        topic = self.topic = get_object_or_404(
            Topic.objects.only('id'),
            id=self.request.query_params['topic_pk'],
        )

        return self.queryset.filter(topic=topic)

    def create(self, *args, **kwargs):
        self.request.data['author'] = self.request.user.id
        self.request.topic['topic'] = self.topic.id

        return super(TopicViewSet, self).create(*args, **kwargs)
