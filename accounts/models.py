from django.db import models
from django.dispatch import receiver

from enhancements.auth.models import AbstractUser, UserManager
from enhancements.models.fields import EnumField
from enhancements.shortcuts import _
from enhancements.models import QuerySet
from enhancements.models.mixins import AutoCleanMixin, PermsMixin


from .consts import UserType, BureauType


class UserQuerySet(QuerySet):

    def governments(self):
        return self.filter(user_type=UserType.government)

    def governments_or(self, user):
        return self.filter(
            models.Q(user_type=UserType.government) |
            models.Q(pk=user.pk)
        )


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

    objects = UserQuerySet.as_manager(UserManager)

    REQUIRED_FIELDS = ['nickname']

    INVISIBLE_FIELDS = {
        'accounts.view_userdata': ['user_data']
    }

    def _clean_bureau_type(self):
        if self.user_type != UserType.bureau:
            self.bureau_type = BureauType.none

    def _check_user_data(self):
        if self.user_type == UserType.company:
            if self.user_data is None:
                self.user_data = UserData.objects.create()
                self.save()
        elif self.user_data is not None:
            self.user_data.delete()

    def clean(self):
        self._clean_bureau_type()
        self._check_user_data()

    @property
    def category(self):
        """
        Return a (user_type, bureau_type) tuple.

        Returns:
            tuple
        """
        return (UserType(self.user_type), BureauType(self.bureau_type))


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
