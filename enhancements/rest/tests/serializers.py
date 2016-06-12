from .models import Goods

from rest_framework import serializers
from enhancements.rest import registry


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods

registry.register(Goods, GoodsSerializer)
