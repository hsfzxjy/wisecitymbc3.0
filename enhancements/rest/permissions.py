from rest_framework.permissions import DjangoObjectPermissions


class DjangoObjectPermissionOrAnonReadOnly(DjangoObjectPermissions):

    authenticated_users_only = False
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_object_permission(self, request, view, obj):
        if getattr(view, '_ignore_object_permissions', False):
            return True

        return super(DjangoObjectPermissionOrAnonReadOnly, self)\
            .has_object_permission(request, view, obj)
