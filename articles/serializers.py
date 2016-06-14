from rest_framework import serializers

from .models import Article, Tag

from enhancements.rest import registry


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        extra_kwargs = {
            'author': {
                'fields': ['id', 'username', 'nickname']
            }
        }


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag

registry.register(Article, ArticleSerializer)
registry.register(Tag, TagSerializer)
