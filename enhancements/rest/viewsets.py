from enhancements.rest import registry

from rest_framework import filters
from rest_framework.response import Response


class RelViewSetMixin(object):

    def get_owner(self, request):
        return super(RelViewSetMixin, self).get_owner(request)

    def get_rel(self, owner):
        return super(RelViewSetMixin, self).get_rel(owner)

    def get_queryset(self):
        self.rel = self.get_rel(self.get_owner(self.request))

        return self.rel.all()

    def perform_create(self, serializer):
        obj = serializer.save()
        self.rel.add(obj)

    def perform_destroy(self, instance):
        self.rel.remove(instance)

        return super(RelViewSetMixin, self).perform_destroy(instance)


def rel_viewset(viewset_class):

    class wrapped_class(RelViewSetMixin, viewset_class):
        pass

    return wrapped_class


class EnhancedViewSetMixin(object):

    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('id',)
    ordering = 'id'
    filter_fields = ()

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
            dict(
                zip(
                    ('fields', 'exclude'),
                    self._get_dynamic_fields_options()
                )
            )
        )

        return serializer_class(*args, **kwargs)

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
