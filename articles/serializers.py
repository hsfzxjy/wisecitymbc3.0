from enhancements.rest import serializers

from .models import Article, Tag


@serializers.register(Article)
class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            'author': {
                'fields': ['id', 'username', 'nickname', 'url']
            }
        }
        slug = {
            'tags': 'name'
        }


@serializers.register(Tag)
class TagSerializer(serializers.ModelSerializer):
    pass
