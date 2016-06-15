from rest_framework import viewsets
from rest_framework.decorators import list_route

from enhancements.rest.urls import register

from .models import Article, Tag

from watson import search as watson


@register(
    'articles',
)
class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    filter_fields = ('article_type', )
    keyword_param = 'keyword'

    def patch_author(self, request):
        request.data.update(dict(author=request.user.id))

    def create(self, request, *args, **kwargs):
        self.patch_author(request)

        return super(ArticleViewSet, self).create(request, *args, **kwargs)

    def filter_queryset(self, qs):
        keyword = self.request.query_params.get(self.keyword_param, '')

        if not self.action == 'search' or not keyword:
            return super(ArticleViewSet, self).filter_queryset(qs)

        return watson.filter(
            qs,
            keyword
        )

    @list_route(['GET'])
    def search(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@register('tags')
class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    filter_fields = ('name', )
