from rest_framework import viewsets, mixins
from rest_framework.exceptions import ParseError
from rest_framework.decorators import list_route

from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.contrib import auth

from enhancements.rest import urls
from enhancements.rest.viewsets import rel_viewset

from files.viewsets import FileViewSet

from .models import User, UserData


@urls.register(
    'users',
)
class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):

    queryset = User.objects.all()
    filter_fields = ('user_type',)

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        arg = self.kwargs[lookup_url_kwarg]

        if arg == 'me':
            if self.request.user.is_authenticated():
                return self.request.user
            else:
                raise Http404

        return super(UserViewSet, self).get_object()

    @list_route(['POST'], permission_classes=[])
    def login(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if user is None:
            raise ParseError('username or password error.')
        else:
            auth.login(request, user)
            return self.render_object(user)

    @list_route(['GET'])
    def logout(self, request, *args, **kwargs):
        auth.logout(request)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class UserNestedGetOwnerMixin(object):

    def get_owner(self, request):
        arg = self.kwargs['user_pk']

        if arg == 'me':
            user = self.request.user
        else:
            user = User.objects.get(pk=arg)

        if user.user_data is None:
            raise Http404

        if not self.request.user.has_perm('accounts.view_userdata', user):
            self.permission_denied(self.request)

        return user


@urls.register_nested(
    'reports',
    UserViewSet,
    'users',
    'user'
)
@rel_viewset
class ReportsViewSet(FileViewSet, UserNestedGetOwnerMixin):

    def get_rel(self, owner):
        return owner.user_data.reports


@urls.register_nested(
    'userdata',
    UserViewSet,
    'users',
    'user',
    routes=[
        dict(
            url=r'^{prefix}/$',
            mapping={'get': 'retrieve', 'patch': 'partial_update'},
            name='{basename}-detail',
            initkwargs={'suffix': 'List'}
        ),
    ]
)
class UserDataViewSet(viewsets.GenericViewSet,
                      mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      UserNestedGetOwnerMixin):

    queryset = UserData.objects.all()

    def get_object(self):
        user = self.get_owner(self.request)

        return user.user_data
