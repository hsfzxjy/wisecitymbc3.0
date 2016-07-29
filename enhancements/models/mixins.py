class AutoCleanMixin(object):

    def save(self, *args, **kwargs):
        self.full_clean()

        return super(AutoCleanMixin, self).save(*args, **kwargs)


def get_all_fields(model_class):
    return set(field.name for field in model_class._meta.get_fields())


class LimitedAccessMixin(object):
    """Permission Enhancement Mixin
    """

    # Format
    # {
    #      <perm>: list of fields disallowed without the permission
    # }
    NON_ACCESSIBLE = {}

    @classmethod
    def _get_non_accessible_fields(cls):
        if hasattr(cls, '_perms_map'):
            return cls._perms_map

        pmap = cls._perms_map = {}
        all_fields = get_all_fields(cls)

        for perms, fields in cls.NON_ACCESSIBLE.items():

            assert isinstance(perms, (str, tuple, list)), (
                "Permission must be a string, list or tuple, "
                "got %r." % type(perms)
            )

            if isinstance(perms, str):
                perms = (perms, )

            for perm in perms:
                pmap[perm] = all_fields & set(fields)

        return pmap

    @classmethod
    def accessible_fields(cls, user, obj=None):
        fields = get_all_fields(cls)

        for perm, invisible in cls._get_non_accessible_fields().items():
            if not user.has_perm(perm, obj):
                fields -= invisible

        return fields
