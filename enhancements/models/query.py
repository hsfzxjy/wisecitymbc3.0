from django.db.models import Manager, QuerySet as QS_


class QuerySet(QS_):

    @classmethod
    def as_manager(cls, base=None):
        if base is None:
            base = Manager

        manager = base.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True
