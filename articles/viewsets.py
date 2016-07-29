from django.shortcuts import get_object_or_404

from enhancements.rest import viewsets

from enhancements.rest.urls import register

from files.viewsets import FileViewSet

from .models import Article, Tag


@register('articles',)
class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    filter_fields = ('article_type', 'author__id', 'tags__id')
    ordering = ('-is_top', '-created_time',)

    def patch_author(self, request):
        request.data.update(dict(author=request.user.id))

    def create(self, request, *args, **kwargs):
        self.patch_author(request)

        return super(ArticleViewSet, self).create(request, *args, **kwargs)


@register('tags')
class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    filter_fields = ('name', )


@register('reports', ArticleViewSet)
class AttachmentsViewSet(FileViewSet):

    ordering = ('-created_time',)

    def get_owner(self, request):
        pk = request.kwargs['article_pk']

        return get_object_or_404(Article, pk=pk)
