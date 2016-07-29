from django.core.exceptions import ValidationError

from rest_framework.fields import SkipField
from rest_framework import serializers as serializers_
from rest_framework.utils.field_mapping import (get_nested_relation_kwargs,
                                                get_relation_kwargs)

from enhancements.entries import BaseDictEntries

from . import serializer_fields


class SerializerEntries(BaseDictEntries):

    def _post_register(self, model, serializer_class):
        if not hasattr(serializer_class, 'Meta'):
            serializer_class.Meta = type('Meta', (), {})

        serializer_class.Meta.model = model

(default_entries,
    register,
    unregister,
    exists,
    get_serializer
 ) = SerializerEntries.expose()


def remove_fields(serializer, fields, disallowed):
    existing = set(serializer.fields.keys())

    if disallowed:
        to_pop = existing & set(fields)
    else:
        to_pop = existing - set(fields)

    to_pop -= set(['id'])

    for field_name in to_pop:
        serializer.fields.pop(field_name)


class DynamicSerializerMixin(object):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        assert not (fields is not None and
                    exclude is not None), (
            'Either `fields` or `exclude` can be passed to the '
            'serializer.'
        )

        super(DynamicSerializerMixin, self).__init__(*args, **kwargs)

        if fields is not None:
            remove_fields(self, fields, disallowed=False)
            return

        if exclude is not None:
            remove_fields(self, exclude, disallowed=True)
            return


class NestedSerializerMixin(object):

    def __init__(self, *args, **kwargs):
        self.slug_relations = getattr(self.Meta, 'slug', {})

        assert isinstance(self.slug_relations, dict), (
            '`Meta.slug` must be a dict, got %r.' % type(self.slug_relations)
        )

        self.Meta.list_serializer_class = ListSerializer

        super(NestedSerializerMixin, self).__init__(*args, **kwargs)

    def get_default_field_names(self, *args, **kwargs):
        return super(NestedSerializerMixin,
                     self).get_default_field_names(*args, **kwargs) + \
            getattr(self.Meta, 'reverse_fields', [])

    def _build_relational_field(self, field_name, relation_info):
        if field_name in self.slug_relations:
            return self._build_slug_field(field_name, relation_info)
        else:
            return self._build_nested_field(field_name, relation_info)

    def _build_slug_field(self, field_name, relation_info):
        field_kwargs = get_relation_kwargs(
            field_name, relation_info)

        field_kwargs.pop('to_field', None)
        field_kwargs.pop('view_name', None)
        field_kwargs['slug_field'] = self.slug_relations[field_name]

        return serializer_fields.SlugRelatedField, field_kwargs

    def _build_nested_field(self, field_name, relation_info):
        model = relation_info.related_model
        serializer_class = get_serializer(model)

        assert serializer_class is not None, (
            'Serializer for model %r is not registered.' % model
        )

        field_kwargs = get_nested_relation_kwargs(relation_info)
        field_kwargs.pop('read_only', None)
        field_kwargs['context'] = self._context

        return serializer_class, field_kwargs

    def build_nested_field(self, field_name, relation_info, nested_depth):
        return self._build_relational_field(field_name, relation_info)

    def build_relational_field(self, field_name, relation_info):
        return self._build_relational_field(field_name, relation_info)

    def to_internal_value(self, data):
        if isinstance(data, int):
            return data

        return super(NestedSerializerMixin, self).to_internal_value(data)

    def validate(self, data):
        model = self.Meta.model
        qs = model.objects.only('id')

        if isinstance(data, int):
            try:
                return qs.get(pk=data)
            except model.DoesNotExist:
                raise ValidationError(
                    'Object with pk=%d does not exist.' % data
                )
        else:
            return data


class LimitedAccessSerializerMixin(object):
    """
    The core implementation of disallowing fields by permissions
    """

    def __init__(self, *args, **kwargs):
        super(LimitedAccessSerializerMixin, self).__init__(*args, **kwargs)

        if 'request' not in self._context:
            return

        request = self._context['request']
        model = self.Meta.model

        if not hasattr(model, 'accessible_fields'):
            return

        allowed = model.accessible_fields(request.user, self.instance) | \
            set(self._declared_fields.keys())
        remove_fields(self, allowed, disallowed=False)


class AutoURLSerializerMixin(serializers_.ModelSerializer):

    url = serializers_.SerializerMethodField()

    def get_url(self, instance):
        return getattr(instance, 'get_absolute_url', lambda: '')()


class AutoPermsSerializerMixin(serializers_.ModelSerializer):

    perms = serializers_.SerializerMethodField()

    def get_perms(self, instance):
        request = self._context.get('request', None)

        if request is None:
            return {}

        user = request.user
        meta = self.Meta.model._meta
        app_label, model_name = meta.app_label, meta.model_name

        perms = {}
        for action in ['add', 'change', 'delete', 'view']:
            perms[action] = user.has_perm(
                '{0}.{1}_{2}'.format(app_label, action, model_name.lower()),
                instance
            )

        return perms


class ListSerializer(serializers_.ListSerializer):

    def __init__(self, *args, **kwargs):
        super(ListSerializer, self).__init__(*args, **kwargs)

        self.required = False

    def run_validation(self, data):
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            raise SkipField

        return super(ListSerializer, self).run_validation(data)

    def to_internal_value(self, data):
        if all(map(lambda x: isinstance(x, int), data)):
            model = self.child.Meta.model

            return model.objects.only('id').filter(pk__in=data)

        return super(ListSerializer, self).to_internal_value(data)


class ModelSerializer(DynamicSerializerMixin,
                      NestedSerializerMixin,
                      LimitedAccessSerializerMixin,
                      AutoURLSerializerMixin,
                      AutoPermsSerializerMixin,
                      serializers_.ModelSerializer):
    pass
