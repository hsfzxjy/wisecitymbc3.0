from rest_framework import serializers

from .models import Article, Tag

from enhancements.rest import registry


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        extra_kwargs = {
            'author': {
                'fields': ['id', 'username', 'nickname', 'url']
            },
            'tags': {
                'slug_field': 'name'
            }
        }
        slug_relations = ['tags']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag

registry.register(Article, ArticleSerializer)
registry.register(Tag, TagSerializer)
