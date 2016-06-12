from .models import Child, Goods, Bucket

from rest_framework import viewsets

from enhancements.rest.urls import register


@register('users', base_name='child')
class V(viewsets.ModelViewSet):

    model = Child


@register('goods')
class GoodsViewSet(viewsets.ModelViewSet):

    queryset = Goods.objects.all()


@register('buckets')
class BucketViewSet(viewsets.ModelViewSet):

    queryset = Bucket.objects.all()
