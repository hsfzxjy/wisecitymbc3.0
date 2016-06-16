from rest_framework.permissions import DjangoObjectPermissions


class DjangoObjectPermissionOrAnonReadOnly(DjangoObjectPermissions):

    authenticated_users_only = False
