from django.db import models, transaction
from jsonfield import JSONField

from django.db.models.signals import post_save
from django.dispatch import receiver

from contextlib import contextmanager


class RevisionBase(models.Model):

    updated_time = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True

    def undo(self):
        with transaction.atomic(), self.manually_save():
            try:
                last_log = self.log_class.objects.filter(
                    owner=self).order_by('-created_time')[1]
            except IndexError:
                # There is only one log left.
                return

            self.current_log.delete()

            self.current_log = last_log
            self.updated_time = last_log.created_time
            self._recover(last_log.serialized_data)

            self.save()

    def __init__(self, *args, **kwargs):
        self.manually_saving = False

        return super(RevisionBase, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def _recover(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def get_log_values(self):
        return {
            field_name: getattr(self, field_name)
            for field_name in self.log_fields_names
        }

    def has_changed(self):

        from .utils import diff

        if self.current_log is None:
            return True

        return bool(diff(self.get_log_values(),
                         self.current_log.serialized_data))

    def create_log(self):
        with transaction.atomic(), self.manually_save():
            log_values = self.get_log_values()
            new_log = self.log_class.objects.create(
                owner=self, serialized_data=log_values, **log_values)
            self.current_log = new_log
            self.updated_time = new_log.created_time
            self.save()

    @contextmanager
    def manually_save(self):
        self.manually_saving = True
        yield
        self.manually_saving = False


class LogBase(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)
    serialized_data = JSONField()

    class Meta:
        abstract = True


def create_revision_model(name, fields, log_fields_names, module,
                          bases=(), log_bases=(), meta=None, log_meta=None):
    '''
    name: str. must be capitalized.
    fields: dict of str:Field.
    log_fields_names: list of str, indicating names of fields.
    module: str. Indicating the module name.

    returns: (revision_class, log_class)
    '''

    log_class_name = name + 'Log'

    fields.update({
        '__module__': module,
        'current_log': models.ForeignKey(
            log_class_name, null=True, blank=True,
            on_delete=models.SET_NULL, editable=False)
    })

    if meta is not None:
        fields.update(Meta=meta)

    revision_class = type(
        name,
        (RevisionBase,) + bases,
        fields
    )

    log_fields = {
        name: field
        for name, field in fields.items() if name in log_fields_names
    }

    log_fields.update({
        'owner': models.ForeignKey(revision_class),
        '__module__': module
    })

    if log_meta is not None:
        log_fields.update(Meta=log_meta)

    log_class = type(
        log_class_name,
        (LogBase, ) + log_bases,
        log_fields
    )

    revision_class.log_class = log_class
    revision_class.log_fields_names = log_fields_names

    return revision_class, log_class


@receiver(post_save)
def revision_pre_save(sender, instance, created,
                      raw, using, update_fields, **kwargs):

    if not issubclass(sender, RevisionBase) or instance.manually_saving \
            or not instance.has_changed():
        return

    instance.create_log()
