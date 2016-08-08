from enhancements.collections import Enum
from enhancements.rest.serializer_fields import EnumField
from enhancements.rest.serializers import ModelSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase


class MyEnum(Enum):

    item = 1


class EnumSerializer(ModelSerializer):

    item = EnumField()


class TestEnum(APITestCase):

    def test_render(self):
        data = {'item': MyEnum.item}
        rendered = JSONRenderer().render(data)
        self.assertEqual(rendered, b'{"item":1}')
