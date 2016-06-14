from rest_framework import viewsets

from enhancements.rest.urls import register

from .models import Article, Tag


@register(
    'articles',
)
class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    filter_fields = ('article_type', )

    def patch_author(self, request):
        request.data.update(dict(author=request.user.id))

    def create(self, request, *args, **kwargs):
        self.patch_author(request)

        return super(ArticleViewSet, self).create(request, *args, **kwargs)


@register('tags')
class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    filter_fields = ('name', )
