from rest_framework import serializers

from enhancements.models.fields import EnumField as ModelEnumField

from django.utils.encoding import smart_text
from django.core.exceptions import ObjectDoesNotExist


class EnumField(serializers.Field):

    def to_representation(self, obj):
        return obj.value

mapping = {
    ModelEnumField: EnumField
}


class SlugRelatedFieldPatch(object):

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
            # self.fail('does_not_exist', slug_name=self.slug_field,
            #           value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


def monkey_patch():
    serializers.SlugRelatedField = type(
        'SlugRelatedField',
        (SlugRelatedFieldPatch, serializers.SlugRelatedField),
        {}
    )
