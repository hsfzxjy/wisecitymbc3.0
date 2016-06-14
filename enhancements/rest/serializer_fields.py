from rest_framework import serializers

from enhancements.models.fields import EnumField as ModelEnumField

class EnumField(serializers.Field):

    def to_representation(self, obj):
        return obj.value

mapping = {
    ModelEnumField: EnumField
}