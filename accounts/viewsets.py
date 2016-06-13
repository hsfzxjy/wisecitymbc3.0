from rest_framework import viewsets, mixins
from django.http import Http404

from enhancements.rest import urls

from .models import User, UserData


@urls.register(
    'users',
)
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        arg = self.kwargs[lookup_url_kwarg]

        if arg == 'me':
            if self.request.user.is_authenticated():
                return self.request.user
            else:
                raise Http404

        return super(UserViewSet, self).get_object()


@urls.register_nested(
    'userdata',
    UserViewSet,
    'users',
    'user',
    routes=[
        dict(
            url=r'^{prefix}/$',
            mapping={'get': 'retrieve', 'patch':'partial_update'},
            name='{basename}-detail',
            initkwargs={'suffix': 'List'}
        ),
    ]
)
class UserDataViewSet(viewsets.GenericViewSet,
                      mixins.RetrieveModelMixin, mixins.UpdateModelMixin):

    queryset = UserData.objects.all()

    def get_object(self):
        arg = self.kwargs['user_pk']

        if arg == 'me':
            user = self.request.user
        else:
            user = User.objects.get(pk=arg)

        if user.user_data is None:
            raise Http404

        if not self.request.user.has_perm('accounts.view_user_data', user):
            self.permission_denied(self.request)

        return user.user_data
