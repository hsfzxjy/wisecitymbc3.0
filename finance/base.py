from django.db import models
from jsonfield import JSONField

from django.db.models.signals import post_save
from django.dispatch import receiver


class RevisionBase(models.Model):

    def undo(self):
        pass

    class Meta:
        abstract = True


class LogBase(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)
    serialized_data = JSONField()

    class Meta:
        abstract = True


def create_revision_model(name, fields, log_fields_names, module,
                          bases=(), log_bases=()):
    '''
    name: str. must be capitalized.
    fields: dict of str:Field.
    log_fields_names: list of str, indicating names of fields.
    module: str. Indicating the module name.

    returns: (revision_class, log_class)
    '''

    fields.update({
        '__module__': module
    })

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

    log_class = type(
        name + 'Log',
        (LogBase, ) + log_bases,
        log_fields
    )

    revision_class.log_class = log_class
    revision_class.log_fields_names = log_fields_names

    return revision_class, log_class


@receiver(post_save)
def revision_pre_save(sender, instance, created,
                      raw, using, update_fields, **kwargs):

    if not issubclass(sender, RevisionBase):
        return

    data = {
        name: getattr(instance, name)
        for name in sender.log_fields_names
    }

    sender.log_class.objects.create(
        owner=instance, serialized_data=data, **data)
