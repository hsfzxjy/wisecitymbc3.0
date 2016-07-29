from django.db import models

from enhancements.auth.models import AbstractUser, UserManager as UserManager_
from enhancements.models.fields import EnumField
from enhancements.shortcuts import _
from enhancements.models import QuerySet
from enhancements.models.mixins import AutoCleanMixin, LimitedAccessMixin

from django.core.exceptions import ValidationError


from .consts import UserType, BureauType


class UserQuerySet(QuerySet):

    def governments(self):
        return self.filter(user_type=UserType.government)

    def governments_or(self, user):
        return self.filter(
            models.Q(user_type=UserType.government) |
            models.Q(pk=user.pk)
        )


class UserManager(UserManager_.from_queryset(UserQuerySet)):

    use_in_migrations = True

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('user_type', UserType.government)

        return super(UserManager, self).create_superuser(
            username, password, **extra_fields)


class User(AutoCleanMixin, LimitedAccessMixin, AbstractUser):

    nickname = models.CharField(_('nickname'), max_length=255, unique=True)
    user_type = EnumField(
        UserType,
        verbose_name=_('user type'),
        default=UserType.company,
        editable=True
    )
    bureau_type = EnumField(
        BureauType,
        verbose_name=_('bureau type'),
        default=BureauType.none,
        editable=True
    )
    user_data = models.OneToOneField(
        'UserData',
        verbose_name=_('user data'),
        null=True,
        blank=True
    )

    objects = UserManager()

    REQUIRED_FIELDS = ['nickname']

    NON_ACCESSIBLE = {
        'accounts.view_userdata': ['user_data']
    }

    def _clean_user_type(self):
        if self.is_superuser:
            self.user_type = UserType.government

    def _clean_staff(self):
        self.is_staff = self.user_type != UserType.company

    def _clean_bureau_type(self):
        if self.user_type != UserType.bureau and \
                self.bureau_type != BureauType.none:
            raise ValidationError({
                'bureau_type': _('non-bureau user cannot have bureau type')
            })

    def _check_user_data(self):
        if self.user_type == UserType.company:
            if self.user_data is None:
                self.user_data = UserData.objects.create()
        elif self.user_data is not None:
            self.user_data.delete()

    def clean(self):
        self._clean_user_type()
        self._clean_staff()
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
