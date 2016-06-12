from rest_framework.utils.field_mapping import get_nested_relation_kwargs, \
    get_relation_kwargs
from enhancements.globalreg.core import RegistryBase

from rest_framework import serializers as serializers_


class SerializerRegistry(RegistryBase):

    def make_key(self, key):
        return key.__name__

registry = SerializerRegistry()


def remove_fields(serializer, fields, disallowed):
    existing = set(serializer.fields.keys())

    if disallowed:
        to_pop = existing & set(fields)
    else:
        to_pop = existing - set(fields)

    for field_name in to_pop:
        serializer.fields.pop(field_name)


class DynamicSerializerMixin(object):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        super(DynamicSerializerMixin, self).__init__(*args, **kwargs)

        if fields is not None:
            remove_fields(self, fields, disallowed=False)
            return

        if exclude is not None:
            remove_fields(self, exclude, disallowed=True)
            return


class NestedEnhancementMixin(object):

    def __init__(self, *args, **kwargs):
        self.pk_relations = set(getattr(self.Meta, 'pk_relations', []))
        self.url_relations = getattr(self.Meta, 'url_relations', [])

        super(NestedEnhancementMixin, self).__init__(*args, **kwargs)

    def build_field(self, field_name, info, model_class, nested_depth):
        """
        COPY FROM `rest_framework.serializers.ModelSerializer.build_field`

        Return a two tuple of (cls, kwargs) to build a serializer field with.
        """
        if field_name in info.fields_and_pk:
            model_field = info.fields_and_pk[field_name]
            return self.build_standard_field(field_name, model_field)

        # Customize

        elif field_name in info.relations:
            relation_info = info.relations[field_name]
            if field_name in self.url_relations or \
                    field_name in self.pk_relations:
                return self.build_relational_field(
                    field_name, relation_info)
            else:
                return self.build_nested_field(
                    field_name, relation_info, nested_depth)

        # End Customize

        elif hasattr(model_class, field_name):
            return self.build_property_field(field_name, model_class)

        elif field_name == self.url_field_name:
            return self.build_url_field(field_name, model_class)

        return self.build_unknown_field(field_name, model_class)

    def build_nested_field(self, field_name, relation_info, nested_depth):
        model = relation_info.related_model
        serializer = registry.get_value(model)

        if serializer is None:
            serializer = type(
                'NestedSerializer',
                (serializers_.ModelSerializer,),
                dict(
                    Meta=type(
                        'Meta',
                        (object, ),
                        dict(model=model)
                    )
                )
            )

        field_kwargs = get_nested_relation_kwargs(relation_info)

        return serializer, field_kwargs

    def build_relational_field(self, field_name, relation_info):
        if field_name in self.pk_relations:
            field_class = serializers_.PrimaryKeyRelatedField
        elif field_name in self.url_relations:
            field_class = serializers_.HyperlinkedRelatedField

        field_kwargs = get_relation_kwargs(
            field_name, relation_info)

        to_field = field_kwargs.pop('to_field', None)
        if to_field and \
                not relation_info.related_model\
                ._meta.get_field(to_field).primary_key:
            field_kwargs['slug_field'] = to_field
            field_class = self.serializer_related_to_field

        # `view_name` is only valid for hyperlinked relationships.
        if not issubclass(
                field_class, serializers_.HyperlinkedRelatedField):
            field_kwargs.pop('view_name', None)

        return field_class, field_kwargs


class PartialFieldsMixin(object):
    """
    The core implementation of disallowing fields by permissions
    """

    def __init__(self, *args, **kwargs):
        super(PartialFieldsMixin, self).__init__(*args, **kwargs)

        if 'request' not in self._context:
            return

        request = self._context['request']
        model = self.Meta.model

        # Backward capibility
        if not hasattr(model, 'get_fields_by_user'):
            return

        allowed = model.get_fields_by_user(request.user, self.instance)
        remove_fields(self, allowed, disallowed=False)


def monkey_patch():
    from rest_framework import serializers

    old_model_serializer = serializers.ModelSerializer

    for object_name in dir(serializers):
        if not object_name.endswith('Serializer'):
            continue

        old_class = getattr(serializers, object_name)
        if not issubclass(old_class, old_model_serializer):
            continue

        new_class = type(
            object_name,
            (DynamicSerializerMixin,
                NestedEnhancementMixin,
                PartialFieldsMixin,
                old_class),
            {}
        )

        setattr(serializers, object_name, new_class)
