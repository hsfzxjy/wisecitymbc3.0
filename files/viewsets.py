from .utils import get_upload_token
from .models import File

from enhancements.rest import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from enhancements.rest.urls import register


@register('uptoken/')
class UpTokenView(APIView):

    _ignore_model_permissions = True

    def get(self, request):
        return Response({
            'uptoken': get_upload_token()
        })


@register('files')
class FileViewSet(viewsets.ModelViewSet):

    queryset = File.objects.all()
