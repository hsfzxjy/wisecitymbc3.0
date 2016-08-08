from rest_framework import serializers

from enhancements.models.fields import EnumField as ModelEnumField


class EnumField(serializers.Field):

    def to_representation(self, obj):
        return obj.value

mapping = {
    ModelEnumField: EnumField
}


class SlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(
                **{self.slug_field: data}
            )[0]
        except (TypeError, ValueError):
            self.fail('invalid')
