from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.decorators import list_route, detail_route

from .models import Notification

from enhancements.rest.urls import register

from django.http import Http404
from django.http.response import HttpResponsePermanentRedirect


@register('n')
class NotificationViewSet(viewsets.ModelViewSet):

    queryset = Notification.objects.all()
    filter_fields = ('module', 'has_read')
    ordering = ('has_read', '-created_time')

    def get_queryset(self):
        # return self.queryset
        if not self.request.user.is_authenticated():
            raise Http404

        return self.queryset.filter(user=self.request.user)

    @list_route(['GET'])
    def mark_as_read(self, request, *args, **kwargs):
        ids = request.query_params.get('ids', [])

        if ids:
            try:
                ids = list(map(int, ids.split(',')))
            except ValueError:
                raise ParseError('ids must be comma-separated ints.')

        qs = self.filter_queryset(self.get_queryset())
        qs.mark_as_read(ids)

        return Response({'status': 'OK'})

    @detail_route(['GET'])
    def redirect(self, request, *args, **kwargs):
        notification = self.get_object()

        notification.mark_as_read()

        return HttpResponsePermanentRedirect(notification.url)
