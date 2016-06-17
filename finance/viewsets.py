from rest_framework import viewsets, mixins

from enhancements.rest.urls import register, register_nested

from . import models


def create_viewset(name, prefix, parent_lookup):

    model = getattr(models, name)
    log_model = getattr(models, name + 'Log')

    def log_get_queryset(self):
        return self.queryset.filter(
            owner__pk=self.kwargs['%s_pk' % parent_lookup]
        )

    viewset = type(
        '{name}ViewSet',
        (
            viewsets.GenericViewSet,
            mixins.ListModelMixin,
            mixins.RetrieveModelMixin
        ),
        {
            'queryset': model.objects.all()
        }
    )
    register(prefix)(viewset)

    log_viewset = type(
        '%sLogViewSet' % name,
        (
            viewsets.GenericViewSet,
            mixins.ListModelMixin,
            mixins.RetrieveModelMixin,
        ),
        {
            'queryset': log_model.objects.all(),
            'get_queryset': log_get_queryset,
        }
    )

    register_nested(
        'logs',
        viewset,
        prefix,
        parent_lookup
    )(log_viewset)

    return viewset, log_viewset


# Initialization

create_viewset('Stock', 'stocks', 'stock')
create_viewset('Bond', 'bonds', 'bond')
create_viewset('Futures', 'futures', 'future')
create_viewset('RawMaterials', 'raw_materials', 'raw_materials')
