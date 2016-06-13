# compat
from rest_framework.utils import model_meta
from rest_framework.settings import api_settings
import copy
from collections import OrderedDict

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

    def get_fields(self):
        """
        NOTICE: COPYING FROM `rest_framework.serializers.Serializer`.
        Return the dict of field names -> field instances that should be
        used for `self.fields` when instantiating the serializer.
        """
        if self.url_field_name is None:
            self.url_field_name = api_settings.URL_FIELD_NAME

        assert hasattr(self, 'Meta'), (
            'Class {serializer_class} missing "Meta" attribute'.format(
                serializer_class=self.__class__.__name__
            )
        )
        assert hasattr(self.Meta, 'model'), (
            'Class {serializer_class} missing "Meta.model" attribute'.format(
                serializer_class=self.__class__.__name__
            )
        )
        if model_meta.is_abstract_model(self.Meta.model):
            raise ValueError(
                'Cannot use ModelSerializer with Abstract Models.'
            )

        declared_fields = copy.deepcopy(self._declared_fields)
        model = getattr(self.Meta, 'model')
        depth = getattr(self.Meta, 'depth', 0)

        if depth is not None:
            assert depth >= 0, "'depth' may not be negative."
            assert depth <= 10, "'depth' may not be greater than 10."

        # Retrieve metadata about fields & relationships on the model class.
        info = model_meta.get_field_info(model)
        field_names = self.get_field_names(declared_fields, info)

        # Determine any extra field arguments and hidden fields that
        # should be included
        extra_kwargs = self.get_extra_kwargs()
        extra_kwargs, hidden_fields = self.get_uniqueness_extra_kwargs(
            field_names, declared_fields, extra_kwargs
        )

        # Determine the fields that should be included on the serializer.
        fields = OrderedDict()

        for field_name in field_names:
            # If the field is explicitly declared on the class then use that.
            if field_name in declared_fields:
                fields[field_name] = declared_fields[field_name]
                continue

            # Determine the serializer field class and keyword arguments.
            field_class, field_kwargs = self.build_field(
                field_name, info, model, depth
            )

            # Include any kwargs defined in `Meta.extra_kwargs`
            extra_field_kwargs = extra_kwargs.get(field_name, {})
            field_kwargs = self.include_extra_kwargs(
                field_kwargs, extra_field_kwargs
            )

            # Customize
            # Apply parent's context to child serializer
            if issubclass(field_class, serializers_.Serializer):
                field_kwargs['context'] = self._context
            # EndCustomize

            # Create the serializer field.
            fields[field_name] = field_class(**field_kwargs)

        # Add in any hidden fields.
        fields.update(hidden_fields)

        return fields

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
