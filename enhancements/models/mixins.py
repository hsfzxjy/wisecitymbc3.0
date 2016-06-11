class AutoCleanMixin(object):

    def save(self, *args, **kwargs):
        self.full_clean()

        return super(AutoCleanMixin, self).save(*args, **kwargs)


class PermsMixin(object):
    """Permission Enhancement Mixin
    """

    PERMS = {}
    DEFAULT_ID = True

    @classmethod
    def get_perms_map(cls):
        if hasattr(cls, '_perms_map'):
            return cls._perms_map

        pmap = cls._perms_map = {}

        for perms, options in cls.PERMS.items():
            assert isinstance(perms, (str, tuple)), \
                "Permission %r must be list or tuple." % perms

            if isinstance(perms, str):
                perms = (perms, )

            for perm in perms:
                pmap[perm] = cls._get_fields_by_perm(perm, options)

        return pmap

    @classmethod
    def _get_fields_by_perm(cls, perm, options):

        # Type check and options validation
        assert isinstance(options, dict), \
            "`options` for %r must be a dict." % perm
        assert not ('visible' in options and 'invisible' in options), \
            "`visible` and `invisible` cannot appear in the same"\
            " option %r." % perm

        fields = set(field.name for field in cls._meta.get_fields())

        if 'visible' in options:
            fields &= set(options['visible'])

        if 'invisible' in options:
            fields -= set(options['invisible'])

        if cls.DEFAULT_ID:
            fields |= {'id'}

        return fields
