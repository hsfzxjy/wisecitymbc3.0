from django.conf.urls import url
from rest_framework import viewsets, routers

from .models import Base, Child


class V(viewsets.ModelViewSet):

    model = Child

rt = routers.SimpleRouter()

rt.register('users', V, base_name='child')

urlpatterns = rt.urls
