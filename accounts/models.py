from django.db import models
from django.dispatch import receiver

from enhancements.auth.models import AbstractUser
from enhancements.models.fields import EnumField
from enhancements.shortcuts import _
from enhancements.models.mixins import AutoCleanMixin, PermsMixin


from .consts import UserType, BureauType


class User(AutoCleanMixin, PermsMixin, AbstractUser):

    nickname = models.CharField(_('nickname'), max_length=255, unique=True)
    user_type = EnumField(
        UserType,
        verbose_name=_('user type'),
        default=UserType.company,
        editable=False
    )
    bureau_type = EnumField(
        BureauType,
        verbose_name=_('bureau type'),
        default=BureauType.none,
        editable=False
    )
    user_data = models.OneToOneField(
        'UserData',
        verbose_name=_('user data'),
        null=True,
        blank=True
    )

    REQUIRED_FIELDS = ['nickname']

    INVISIBLE_FIELDS = {
        'accounts.view_userdata': ['user_data']
    }

    def _clean_bureau_type(self):
        if self.user_type != UserType.bureau:
            self.bureau_type = BureauType.none

    def clean(self):
        self._clean_bureau_type()

    @property
    def category(self):
        """
        Return a (user_type, bureau_type) tuple.

        Returns:
            tuple
        """
        return (UserType(self.user_type), BureauType(self.bureau_type))


@receiver(models.signals.post_save, sender=User)
def check_user_data(sender, instance, **kwargs):
    if instance.user_type == UserType.company:
        if instance.user_data is None:
            instance.user_data = UserData.objects.create()
            instance.save()
    elif instance.user_data is not None:
        instance.user_data.delete()


class UserData(models.Model):

    name = models.CharField(_('name'), max_length=255, blank=True)
    industry = models.CharField(_('industry'), max_length=255, blank=True)
    sector = models.CharField(_('sector'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    reports = models.ManyToManyField(
        'files.File', verbose_name=_('reports'), blank=True)

    class Meta:
        verbose_name = _('user data')
        verbose_name_plural = _('user data')
