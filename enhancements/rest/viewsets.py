from .serializers import default_entries

from rest_framework import filters
from rest_framework.response import Response
from rest_framework import viewsets


class ViewSetMixin(object):

    nested = False

    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('id',)
    ordering = 'id'
    filter_fields = ()

    def render_list(self, queryset=None, filter=False):
        if queryset is None:
            queryset = self.get_queryset()

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

    def _get_dynamic_fields_options(self):
        """
        Extract `fields` or `exclude` from query params.
        """

        def extract(name):
            option_str = self.request.query_params.get(name, '')\
                .replace(' ', '')

            return option_str.split(',') if option_str else None

        return extract('fields'), extract('exclude')

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs.update(
            dict(zip(
                ('fields', 'exclude'),
                self._get_dynamic_fields_options()
            ))
        )

        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        model = self.get_queryset().model
        serializer_class = default_entries.get(model, None)

        if serializer_class is not None:
            return serializer_class

        return super(ViewSetMixin, self).get_serializer_class()


class ModelViewSet(ViewSetMixin, viewsets.ModelViewSet):
    pass


class GenericViewSet(ViewSetMixin, viewsets.GenericViewSet):
    pass
