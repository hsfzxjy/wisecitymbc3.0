from .utils import get_upload_token
from .models import File

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.response import Response

from enhancements.rest.urls import register_view, register

from django.http.response import HttpResponseRedirect


@register_view('uptoken/')
class UpTokenView(APIView):

    _ignore_model_permissions = True

    def get(self, request):
        return Response({
            'uptoken': get_upload_token()
        })


@register('files')
class FileViewSet(viewsets.ModelViewSet):

    queryset = File.objects.all()

    @detail_route(['GET'])
    def download(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_object().storage_url)