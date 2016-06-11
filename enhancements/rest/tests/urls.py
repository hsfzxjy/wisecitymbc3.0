from django.conf.urls import url
from rest_framework import viewsets, routers

from .models import Base, Child, Goods
from .serializers import GoodsSerializer


class V(viewsets.ModelViewSet):

    model = Child


class GoodsViewSet(viewsets.ModelViewSet):

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

rt = routers.SimpleRouter()

rt.register('users', V, base_name='child')
rt.register('goods', GoodsViewSet, )

urlpatterns = rt.urls
