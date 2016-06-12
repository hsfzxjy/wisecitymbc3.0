from .models import Goods, Bucket

from rest_framework import serializers
from enhancements.rest import registry


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods


class BucketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bucket

registry.register(Goods, GoodsSerializer)
registry.register(Bucket, BucketSerializer)
