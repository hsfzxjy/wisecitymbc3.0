from enhancements.rest import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from enhancements.rest.urls import register

from .models import Reply, Topic
from accounts.consts import UserType


@register('topics')
class TopicViewSet(viewsets.ModelViewSet):

    queryset = Topic.objects.all()
    ordering = ('-updated_time', '-created_time')

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

    @detail_route(['GET'])
    def open(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.open(request.user)
        return Response(self.get_serializer(obj).data)

    @detail_route(['GET'])
    def close(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.close(request.user)
        return Response(self.get_serializer(obj).data)


@register('replies', TopicViewSet)
class ReplyViewSet(viewsets.ModelViewSet):

    nested = True
    queryset = Reply.objects.all()
    ordering = ('-created_time',)

    def get_rel(self):
        self.topic = self.get_parent_object()
        return self.topic.replies

    def create(self, *args, **kwargs):
        topic = self.topic
        self.check_object_permissions(self.request, self.topic)

        self.request.data['author'] = self.request.user.id
        self.request.data['topic'] = topic.id

        return super(ReplyViewSet, self).create(*args, **kwargs)
