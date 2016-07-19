from rest_framework.serializers import ModelSerializer
from enhancements.rest import registry
from .models import Base, Child

from rest_framework.test import APITestCase


class ChildSerializer(ModelSerializer):

    class Meta:
        model = Child
        fields = ('id',)

registry.register(Child, ChildSerializer)


class SerializerTestCase(APITestCase):

    def setUp(self):
        self.child = Child.objects.create(id=2)
        self.base = Base.objects.create(name='1', child=self.child, id=1)

    def test_dynamic(self):
        class BaseSerializer(ModelSerializer):

            class Meta:
                model = Base
                pk_relations = ['child']

        s = BaseSerializer(self.base, exclude=['name', 'child'])
        self.assertDictContainsSubset({'id': 1}, s.data)
        s = BaseSerializer(self.base, fields=['id'])
        self.assertEqual(s.data, {'id': 1})

    def test_pk_rel(self):
        class BaseSerializer(ModelSerializer):

            class Meta:
                model = Base
                pk_relations = ['child']

        s = BaseSerializer(self.base)
        self.assertDictContainsSubset(
            {'id': 1, 'name': '1', 'child': 2}, s.data)

    def test_nested(self):

        class BaseSerializer(ModelSerializer):

            class Meta:
                model = Base

        s = BaseSerializer(self.base)
        self.assertDictContainsSubset(
            {'id': 1, 'name': '1', 'child': {'id': 2}}, s.data)
