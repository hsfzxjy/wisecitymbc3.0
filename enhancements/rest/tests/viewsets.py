from .models import Child, Goods, Bucket, Box, Ball

from rest_framework import viewsets

from enhancements.rest.urls import register, register_nested


@register('users', base_name='child')
class V(viewsets.ModelViewSet):

    model = Child


@register('goods')
class GoodsViewSet(viewsets.ModelViewSet):

    queryset = Goods.objects.all()


@register('buckets')
class BucketViewSet(viewsets.ModelViewSet):

    queryset = Bucket.objects.all()


@register('boxes')
class BoxViewSet(viewsets.ModelViewSet):

    queryset = Box.objects.all()
    ordering_fields = ('id',)


@register_nested(
    'balls',
    BoxViewSet,
    'boxes',
    'box',
)
class BallViewSet(viewsets.ModelViewSet):

    queryset = Ball.objects.all()

    def get_queryset(self):
        return Ball.objects.filter(box=self.kwargs['box_pk'])

    def create(self, request, *args, **kwargs):
        return super(BallViewSet, self).create(request, *args, **kwargs)
