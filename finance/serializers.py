from rest_framework import serializers

from . import models

from enhancements.rest import registry


def create_serializer(name, meta_fields=None):

    model, log_model = getattr(models, name), getattr(models, name + 'Log')

    meta_fields.update(dict(model=model, exclude=('current_log',)))

    serializer = type(
        '{name}Serializer'.format(name=name),
        (serializers.ModelSerializer, ),
        dict(
            Meta=type('Meta', (), meta_fields)
        )
    )

    log_serializer = type(
        '{name}LogSerializer'.format(name=name),
        (serializers.ModelSerializer, ),
        {
            'Meta': type(
                'Meta',
                (),
                {
                    'model': log_model,
                    'exclude': ('owner', 'serialized_data')
                }
            )
        }
    )

    registry.register(model, serializer)
    registry.register(log_model, log_serializer)

    return serializer, log_serializer


StockSerializer, StockLogSerializer = create_serializer('Stock', {
    'reverse_fields': ['comments']
})

BondSerializer, BondLogSerializer = create_serializer('Bond', {})

FuturesSerializer, FuturesLogSerializer = create_serializer('Futures', {})

RawMaterialsSerializer, RawMaterialsLogSerializer = create_serializer(
    'RawMaterials', {})


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        exclude = ('stock', 'perms')

registry.register(models.Comment, CommentSerializer)
