from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import User, UserData

from enhancements.shortcuts import _

from .consts import UserType

from django_object_actions import DjangoObjectActions


class UserDataInline(admin.TabularInline):
    model = UserData


@admin.register(User)
class UserAdmin(DjangoObjectActions, auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'nickname')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nickname',
                       'user_type', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'nickname', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    inlines = []

    def get_inline_instances(self, request, obj=None):
        if obj is not None and obj.user_type == UserType.company.value:
            self.inlines = [UserDataInline]
        else:
            self.inlines = []

        return super(UserAdmin, self).get_inline_instances(request, obj)

    def change_password(self, request, user):
        from django.http import HttpResponseRedirect

        return HttpResponseRedirect('../../password/')

    change_password.label = _('Change Password')
    change_password.short_description = _(
        'Click here to change your password.')

    change_actions = ['change_password']
