from rest_framework.views import APIView
from rest_framework.response import Response

from enhancements.rest import urls

from .utils import *


@urls.register(r'^perms/((?P<app>\w+)/(?P<model>\w+)/((?P<id>\d+)/)?)?$')
class ObjectPermsView(APIView):

    _ignore_model_permissions = True

    def get(self, request, app=None, model=None, id=None):
        if app is None:
            perms_dict = default_perms(request.user)
        else:
            perms_dict = model_perms(request.user, app, model, id)

        return Response(perms_dict)
