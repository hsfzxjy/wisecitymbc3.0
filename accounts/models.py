from django.db import models
from django.dispatch import receiver

from enhancements.auth.models import AbstractUser
from enhancements.models.fields import EnumField
from enhancements.shortcuts import _
from enhancements.models.mixins import AutoCleanMixin


from .consts import UserType, BureauType


class User(AutoCleanMixin, AbstractUser):

    nickname = models.CharField(_('nickname'), max_length=255, unique=True)
    user_type = EnumField(
        UserType,
        verbose_name=_('user type'),
        default=UserType.company)
    bureau_type = EnumField(
        BureauType,
        verbose_name=_('bureau type'),
        default=BureauType.none)

    REQUIRED_FIELDS = ['nickname']

    def _clean_bureau_type(self):
        if self.user_type != UserType.bureau:
            self.bureau_type = BureauType.none

    def clean(self):
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


@receiver(models.signals.post_save, sender=User)
def check_user_data(sender, instance, **kwargs):
    if instance.user_type == UserType.company:
        if instance.data is None:
            UserData.objects.create(user=instance)
    elif instance.data is not None:
        instance.data.delete()


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
