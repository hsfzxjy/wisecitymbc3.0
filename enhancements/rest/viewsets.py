from enhancements.rest import registry

from rest_framework import filters
from rest_framework.response import Response


class EnhancedViewSetMixin(object):

    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('id',)
    ordering = 'id'
    search_fields = ()

    def render_list(self, queryset=None, filter=False):
        if queryset is None:
            queryset = self.get_queryset

        if filter:
            queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def render_object(self, obj=None):
        if obj is None:
            obj = self.get_object()

        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def get_serializer_class(self):
        model = self.get_queryset().model
        serializer_class = registry.get_value(model, None)

        if serializer_class is not None:
            return serializer_class

        return super(EnhancedViewSetMixin, self).get_serializer_class()


def monkey_patch():
    from rest_framework import viewsets

    for object_name in dir(viewsets):
        if not object_name.endswith('ViewSet'):
            continue

        old_class = getattr(viewsets, object_name)

        new_class = type(
            object_name,
            (EnhancedViewSetMixin, old_class,),
            {}
        )

        setattr(viewsets, object_name, new_class)
