from .models import Goods, Bucket, Box, Ball

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


class BoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Box


class BallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ball

registry.register(Ball, BallSerializer)
registry.register(Box, BoxSerializer)
