from django.contrib import admin

from .models import Stock, Bond, Futures, RawMaterials, Comment

from django_object_actions import DjangoObjectActions

from enhancements.shortcuts import _


class BaseAdmin(DjangoObjectActions, admin.ModelAdmin):

    def undo(self, request, obj):
        obj.undo()

    undo.label = _('Undo')
    undo.short_description = _('Revert this object to previous version.')

    change_actions = ('undo', )

admin.site.register(Stock, BaseAdmin)
admin.site.register(Bond, BaseAdmin)
admin.site.register(Futures, BaseAdmin)
admin.site.register(RawMaterials, BaseAdmin)
admin.site.register(Comment)
