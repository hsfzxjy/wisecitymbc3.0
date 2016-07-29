from rest_framework import mixins

from enhancements.rest import viewsets
from enhancements.rest.urls import register

from . import models


def create_viewset(name, prefix):

    model = getattr(models, name)
    log_model = getattr(models, name + 'Log')

    viewset = type(
        '{name}ViewSet',
        (
            viewsets.GenericViewSet,
            mixins.ListModelMixin,
            mixins.RetrieveModelMixin
        ),
        {
            'queryset': model.objects.all(),
            'ordering': ('-updated_time',)
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
            'nested': True,
            'get_rel': lambda self: self.get_parent_object().logs,
            'queryset': log_model.objects.all(),
        }
    )

    register('logs', viewset)(log_viewset)

    return viewset, log_viewset


# Initialization

create_viewset('Stock', 'stocks')
create_viewset('Bond', 'bonds')
create_viewset('Futures', 'futures')
create_viewset('RawMaterials', 'raw_materials')
