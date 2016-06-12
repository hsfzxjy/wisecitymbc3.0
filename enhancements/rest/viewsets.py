from enhancements.rest import registry


class EnhancedViewSetMixin(object):

    def get_serializer_class(self):
        model = self.get_queryset().model
        serializer_class = registry.get_value(model, None)

        if serializer_class is not None:
            return serializer_class

        return super(EnhancedViewSetMixin, self).get_serializer_class()


def monkey_patch():
    from rest_framework import viewsets

    for object_name in dir(viewsets):
        if not object_name.endswith('ViewSet'):
            continue

        old_class = getattr(viewsets, object_name)

        new_class = type(
            object_name,
            (EnhancedViewSetMixin, old_class,),
            {}
        )

        setattr(viewsets, object_name, new_class)
