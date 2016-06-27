class AutoURLMixin(object):

    def get_absolute_url(self):
        from enhancements.rest.reverse import safe_reverse

        name = self.__class__.__name__.lower()

        return safe_reverse(
            'views.{name}-detail'.format(name=name),
            kwargs={'{name}_pk'.format(name=name): self.pk}
        )


class AutoCleanMixin(object):

    def save(self, *args, **kwargs):
        self.full_clean()

        return super(AutoCleanMixin, self).save(*args, **kwargs)


class PermsMixin(object):
    """Permission Enhancement Mixin
    """

    # Format
    # {
    #      <perm>: list of fields disallowed without the permission
    # }
    INVISIBLE_FIELDS = {}
    DEFAULT_ID = True

    @classmethod
    def get_invisible_fields(cls):
        if hasattr(cls, '_perms_map'):
            return cls._perms_map

        pmap = cls._perms_map = {}
        all_fields = set(field.name for field in cls._meta.get_fields())

        for perms, invisible_fields in cls.INVISIBLE_FIELDS.items():
            assert isinstance(perms, (str, tuple)), \
                "Permission %r must be list or tuple." % perms

            if isinstance(perms, str):
                perms = (perms, )

            for perm in perms:
                pmap[perm] = fields = all_fields & set(invisible_fields)

                if cls.DEFAULT_ID:
                    fields -= {'id'}

        return pmap

    @classmethod
    def get_fields_by_user(cls, user, obj=None):
        fields = set(field.name for field in cls._meta.get_fields())

        for perm, invisible in cls.get_invisible_fields().items():
            if not user.has_perm(perm, obj):
                fields -= invisible

        return fields
