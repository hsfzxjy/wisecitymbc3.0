from django.db import models
from django.conf import settings

from enhancements.models.fields import EnumField
from enhancements.models.mixins import PermsMixin, AutoCleanMixin
from enhancements.shortcuts import _

from .consts import ArticleType


class Article(PermsMixin, AutoCleanMixin, models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('author'))
    title = models.CharField(_('title'), max_length=255)
    tags = models.ManyToManyField('Tag', verbose_name=_('tags'), blank=True)
    summary = models.TextField(_('summary'), blank=True)
    content = models.TextField(_('content'))
    is_top = models.BooleanField(_('is top'), default=False)
    created_time = models.DateTimeField(_('created'), auto_now_add=True)
    attachments = models.ManyToManyField(
        'files.File', verbose_name=_('attachments'), blank=True)
    article_type = EnumField(
        ArticleType,
        verbose_name=_('article type'),
        default=ArticleType.government,
    )

    def _clean_type(self):
        self.article_type = ArticleType.from_user(self.author)

    def _clean_content(self):
        from enhancements.utils.html import standardize, summarize

        self.content = standardize(self.content)
        self.summary = summarize(self.content)

    def clean(self):
        self._clean_type()
        self._clean_content()

    def get_absolute_url(self):
        return '/detail/articles/{0}/'.format(self.id)


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)

    def get_absolute_url(self):
        return '/tags/{0}/'.format(self.id)
