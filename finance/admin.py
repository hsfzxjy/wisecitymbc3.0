from django.contrib import admin

from .models import Stock, Bond, Futures, RawMaterials, Comment

from django_object_actions import DjangoObjectActions

from enhancements.shortcuts import _


class CommentInline(admin.TabularInline):

    model = Stock.comments.through


class BaseAdmin(DjangoObjectActions, admin.ModelAdmin):

    def undo(self, request, obj):
        obj.undo()

    undo.label = _('Undo')
    undo.short_description = _('Revert this object to previous version.')

    change_actions = ('undo', )


def create_admin(model, bases=()):

    admin_class = type(
        model.__class__.__name__ + 'Admin',
        bases + (BaseAdmin,),
        {}
    )

    admin.site.register(model, admin_class)

    return admin


class StockAdminMixin(object):

    inlines = [CommentInline]

create_admin(Stock, (StockAdminMixin,))
create_admin(Bond)
create_admin(Futures)
create_admin(RawMaterials)

admin.site.register(Comment)
