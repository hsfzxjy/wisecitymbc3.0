from django.test import TestCase

from .models import (BasicModel, ForeignKeySource,
                     ForeignKeyTarget, ManyToManySource, ManyToManyTarget)

from rest_framework.serializers import ModelSerializer
from rest_framework.test import APIRequestFactory

from enhancements.rest import serializers


class TestRegisterSerializer(TestCase):

    def test_register_and_unregister(self):

        @serializers.register(BasicModel)
        class SerializerClass(serializers.DynamicSerializerMixin,
                              ModelSerializer):
            pass

        self.assertEqual(serializers.get_serializer(
            BasicModel), SerializerClass)

        serializers.unregister(BasicModel)
        self.assertFalse(serializers.exists(BasicModel))


class TestDynamicSerializer(TestCase):

    class BasicModelSerializer(serializers.DynamicSerializerMixin,
                               ModelSerializer):

        class Meta:
            model = BasicModel

    def setUp(self):
        self.instance = BasicModel.objects.create(name='name', text='text')

    def test_fields(self):
        serializer = self.BasicModelSerializer(self.instance, fields=('name',))
        self.assertDictEqual(serializer.data, {
            'id': self.instance.id,
            'name': 'name'
        })

    def test_exclude(self):
        serializer = self.BasicModelSerializer(
            self.instance, exclude=('id', 'text'))
        self.assertDictEqual(serializer.data, {
            'id': self.instance.id,
            'name': 'name'
        })

    def test_fields_conflicts_with_exclude(self):
        try:
            self.BasicModelSerializer(
                self.instance,
                exclude=('name',),
                fields=('id',)
            )
        except AssertionError:
            pass
        else:
            self.fail(
                '`fields` and `exclude` cannot be set at a time.'
            )


class TestNestedSerializer(TestCase):

    def setUp(self):
        @serializers.register(ForeignKeyTarget)
        class ForeignKeyTargetSerializer(serializers.DynamicSerializerMixin,
                                         serializers.NestedSerializerMixin,
                                         ModelSerializer):
            pass

        @serializers.register(ManyToManyTarget)
        class ManyToManyTargetSerializer(serializers.DynamicSerializerMixin,
                                         serializers.NestedSerializerMixin,
                                         ModelSerializer):
            pass

        self.fk_target = ForeignKeyTarget.objects.create(name='fk_target')
        self.fk_source = ForeignKeySource.objects.create(
            target=self.fk_target, name="fk_source")

        self.m2m_target = ManyToManyTarget.objects.create(name='m2m_target')
        self.m2m_source = ManyToManySource.objects.create(name='m2m_source')
        self.m2m_source.targets.add(self.m2m_target)

    def tearDown(self):
        serializers.unregister(ManyToManyTarget)
        serializers.unregister(ForeignKeyTarget)

    class FKSourceSerializer(serializers.NestedSerializerMixin,
                             ModelSerializer):

        class Meta:
            model = ForeignKeySource

    def test_normal_nested(self):
        self.assertDictEqual(self.FKSourceSerializer(self.fk_source).data, {
            'id': self.fk_source.id,
            'name': self.fk_source.name,
            'target': {
                'id': self.fk_target.id,
                'name': self.fk_target.name
            }
        })

    class FKSourceExtraKwargsSerializer(
            serializers.NestedSerializerMixin, ModelSerializer):

        class Meta:
            model = ForeignKeySource
            extra_kwargs = {
                'target': {
                    'fields': ('id', )
                }
            }

    def test_nested_with_extra_kwargs(self):

        self.assertDictEqual(
            self.FKSourceExtraKwargsSerializer(self.fk_source).data, {
                'id': self.fk_source.id,
                'name': self.fk_source.name,
                'target': {
                    'id': self.fk_target.id,
                }
            }
        )

    class FKSourceSlugSerializer(
            serializers.NestedSerializerMixin, ModelSerializer):

        class Meta:
            model = ForeignKeySource
            slug = {
                'target': 'name'
            }

    def test_normal_slug(self):

        self.assertDictEqual(
            self.FKSourceSlugSerializer(self.fk_source).data, {
                'id': self.fk_source.id,
                'name': self.fk_source.name,
                'target': self.fk_target.name
            }
        )

    class FKSourceCustomSlugSerializer(
            serializers.NestedSerializerMixin, ModelSerializer):

        class Meta:
            model = ForeignKeySource
            slug = {
                'target': 'custom_name'
            }

    def test_slug_for_custom_model_property(self):

        self.assertDictEqual(
            self.FKSourceCustomSlugSerializer(self.fk_source).data, {
                'id': self.fk_source.id,
                'name': self.fk_source.name,
                'target': 'custom %s' % self.fk_target.name
            }
        )

    def test_partially_update_nested_serializer(self):
        fk_target = ForeignKeyTarget.objects.create(name='fk_target 2')

        serializer = self.FKSourceSerializer(
            self.fk_source,
            data={
                'target': fk_target.id
            },
            partial=True
        )

        if not serializer.is_valid():
            self.fail(serializer.errors)
        serializer.save()

        self.fk_source.refresh_from_db()
        self.assertEqual(self.fk_source.target.name, 'fk_target 2')

    def test_partially_update_nested_not_found(self):

        fk_target = ForeignKeyTarget.objects.create(name='fk_target 2')

        serializer = self.FKSourceSerializer(
            self.fk_source,
            data={
                'target': fk_target.id + 1
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('not exist.', serializer.errors['target']
                      ['non_field_errors'][0])

    def test_partially_update_slug(self):
        fk_target = ForeignKeyTarget.objects.create(name='fk_target 2')

        serializer = self.FKSourceSlugSerializer(
            self.fk_source,
            data={
                'target': fk_target.name
            },
            partial=True
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        self.fk_source.refresh_from_db()
        self.assertEqual(self.fk_source.target.name, 'fk_target 2')

    class M2MSourceSerializer(
            serializers.NestedSerializerMixin, ModelSerializer):

        class Meta:
            model = ManyToManySource

    def test_m2m_nested(self):

        serializer = self.M2MSourceSerializer(self.m2m_source)
        self.assertDictEqual(serializer.data, {
            'id': self.m2m_source.id,
            'name': self.m2m_source.name,
            'targets': [
                {
                    'id': self.m2m_target.id,
                    'name': self.m2m_target.name,
                }
            ]
        })

    def test_partially_update_m2m_nested(self):

        serializer = self.M2MSourceSerializer(self.m2m_source, {
            'targets': []
        }, partial=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        self.assertEqual(self.m2m_source.targets.count(), 0)

        serializer = self.M2MSourceSerializer(self.m2m_source, {
            'targets': [self.m2m_target.id]
        }, partial=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        self.assertEqual(self.m2m_source.targets.count(), 1)


def mock_request(perms_map):

    request = APIRequestFactory().get('')
    request.user = type(
        'User',
        (object,),
        {
            'has_perm': lambda self, perm, instance=None:
                perms_map.get(perm, False)
        }
    )()

    return request


class TestLimitedAccessSerializer(TestCase):

    def setUp(self):
        self.instance = BasicModel.objects.create(name='name', text='text')

    def test_access_limited_object(self):
        class SerializerClass(serializers.LimitedAccessSerializerMixin,
                              ModelSerializer):

            class Meta:
                model = BasicModel

        request = mock_request({})

        serializer = SerializerClass(
            self.instance, context=dict(request=request))

        self.assertDictEqual(serializer.data, {
            'id': self.instance.id,
            'text': self.instance.text,
        })

        request = mock_request({
            'rest_test.view_basicmodel': True
        })

        serializer = SerializerClass(
            self.instance, context=dict(request=request))

        self.assertDictEqual(serializer.data, {
            'id': self.instance.id,
            'text': self.instance.text,
            'name': self.instance.name
        })

    def test_access_limited_list(self):

        @serializers.register(ManyToManyTarget)
        class M2MTargetSerializer(
                serializers.LimitedAccessSerializerMixin, ModelSerializer):
            pass

        class SerializerClass(serializers.NestedSerializerMixin,
                              ModelSerializer):

            class Meta:
                model = ManyToManySource

        request = mock_request({
            'rest_test.view_manytomanytarget': False
        })

        source = ManyToManySource.objects.create(name='source')
        target = ManyToManyTarget.objects.create(name='target')
        source.targets.add(target)

        serializer = SerializerClass(source, context={'request': request})

        self.assertDictEqual(serializer.data, {
            'id': source.id,
            'name': source.name,
            'targets': [{
                'id': target.id,
            }]
        })

        serializers.unregister(ManyToManyTarget)


class TestAutoURLSerializer(TestCase):

    def test_default(self):
        class SerializerClass(
                serializers.AutoURLSerializerMixin,
                ModelSerializer):
            class Meta:
                model = ManyToManyTarget

        self.assertEqual(
            SerializerClass(
                ManyToManyTarget.objects.create(name='name')
            ).data['url'],
            ''
        )

    def test_auto_url(self):
        class SerializerClass(
                serializers.AutoURLSerializerMixin,
                ModelSerializer):
            class Meta:
                model = BasicModel

        serializer = SerializerClass(
            BasicModel.objects.create(
                name='name'
            )
        )

        self.assertEqual(
            serializer.data['url'],
            'test_url'
        )


class TestAutoPermsSerializer(TestCase):

    def test_auto_perms(self):
        class SerializerClass(serializers.AutoPermsSerializerMixin,
                              ModelSerializer):
            class Meta:
                model = BasicModel

        request = mock_request({
            'rest_test.%s_basicmodel' % action: value
            for action, value in dict(
                view=True,
                add=False,
                change=False,
                delete=True,
            ).items()
        })

        serializer = SerializerClass(
            BasicModel.objects.create(name='name'),
            context=dict(request=request)
        )

        self.assertDictEqual(serializer.data['perms'], {
            'add': False,
            'change': False,
            'delete': True,
            'view': True
        })
