from .models import Child, Goods
from .serializers import GoodsSerializer

from rest_framework import viewsets

from enhancements.rest.urls import register


@register('users', base_name='child')
class V(viewsets.ModelViewSet):

    model = Child


@register('goods')
class GoodsViewSet(viewsets.ModelViewSet):

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
