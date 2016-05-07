class AutoCleanMixin(object):

    def save(self, *args, **kwargs):
        self.full_clean()

        return super(AutoCleanMixin, self).save(*args, **kwargs)
