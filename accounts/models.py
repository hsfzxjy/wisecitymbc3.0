from django.db import models

from enhancements.auth.models import AbstractUser
from enhancements.shortcuts import _, ValidationError
from enhancements.models.mixins import AutoCleanMixin


from .consts import USER_TYPE_CHOICES, \
    UserType, BUREAU_TYPE_CHOICES, BureauType


class User(AutoCleanMixin, AbstractUser):

    nickname = models.CharField(_('nickname'), max_length=255, unique=True)
    user_type = models.IntegerField(
        _('user type'),
        choices=USER_TYPE_CHOICES, default=UserType.company.value)
    bureau_type = models.IntegerField(
        _('bureau type'),
        choices=BUREAU_TYPE_CHOICES, default=BureauType.none.value)

    REQUIRED_FIELDS = ['nickname']

    def _clean_data(self):
        if self.user_type == UserType.company.value:
            if self.data is None:
                UserData.objects.create(user=self)
        elif self.data is not None:
            self.data.delete()

    def _clean_bureau_type(self):
        if self.user_type != UserType.bureau.value:
            self.bureau_type = BureauType.none.value

    def clean(self):
        self._clean_data()
        self._clean_bureau_type()

    @property
    def data(self):
        try:
            user_data = self._data
        except UserData.DoesNotExist:
            user_data = None

        return user_data

    @property
    def category(self):
        """[summary]

        Return a (user_type, bureau_type) tuple.

        Returns:
            tuple
        """
        return (UserType(self.user_type), BureauType(self.bureau_type))


class UserData(models.Model):
    user = models.OneToOneField(
        'User', related_name='_data', null=True, blank=True)
    name = models.CharField(_('name'), max_length=255, blank=True)
    industry = models.CharField(_('industry'), max_length=255, blank=True)
    sector = models.CharField(_('sector'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    reports = models.ManyToManyField(
        'files.File', verbose_name=_('reports'), blank=True)

    class Meta:
        verbose_name = _('user data')
        verbose_name_plural = _('user data')
