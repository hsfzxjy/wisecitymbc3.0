from .models import Goods

from enhancements.rest.serializers import ModelSerializer


class GoodsSerializer(ModelSerializer):

    class Meta:
        model = Goods
