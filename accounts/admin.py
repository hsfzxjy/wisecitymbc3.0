from django.contrib import admin
from django.contrib.auth import admin as auth_admin, \
    forms as auth_forms, models as auth_models

from enhancements.shortcuts import _

from .models import User

from django_object_actions import DjangoObjectActions

from rules.contrib.admin import ObjectPermissionsModelAdmin


def monkey_patch():
    auth_forms.UserChangeForm.clean_password = \
        lambda self: self.initial.get('password')


@admin.register(User)
class UserAdmin(DjangoObjectActions,
                auth_admin.UserAdmin, ObjectPermissionsModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'nickname', 'bureau_type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nickname',
                       'user_type', 'bureau_type',
                       'password1', 'password2'),
        }),
    )
    list_display = ('username', 'nickname', 'user_type', 'bureau_type')
    list_filter = ()
    search_fields = ('username',)
    ordering = ('username',)

    def change_password(self, request, user):
        from django.http import HttpResponseRedirect

        return HttpResponseRedirect('../../password/')

    change_password.label = _('Change Password')
    change_password.short_description = _(
        'Click here to change your password.')

    change_actions = ['change_password']

monkey_patch()

admin.site.unregister(auth_models.Group)
