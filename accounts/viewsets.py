from rest_framework import viewsets

from enhancements.rest import urls

from .models import User, UserData


@urls.register(
    'users',
)
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
