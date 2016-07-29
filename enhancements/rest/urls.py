from rest_framework.routers import DefaultRouter, Route
from rest_framework.views import APIView

from rest_framework_nested.routers import NestedSimpleRouter

from .viewsets import ViewSetMixin

from django.conf.urls import url


def is_view(cls):
    return issubclass(cls, APIView) and not is_viewset(cls)


def is_viewset(cls):
    return issubclass(cls, ViewSetMixin)


def get_router_class(routes, base, default):
    if routes is None:
        return default

    return type(
        'CustomRouter',
        (base,),
        dict(routes=[
            Route(**route_option) for route_option in routes
        ])
    )


def associate_viewset_with_router(viewset, router, pattern, base_name):
    viewset._route_info = (
        pattern,
        base_name if base_name is not None else router.get_default_base_name(
            viewset)
    )


class NestedViewSetMixin(object):

    @property
    def rel(self):
        if hasattr(self, '_rel'):
            return self._rel

        self._rel = self.get_rel() if hasattr(self, 'get_rel') else None

        return self._rel

    def get_queryset(self):
        rel = self.rel

        return (rel.all()
                if rel
                else super(NestedViewSetMixin, self).get_queryset())

    def perform_create(self, serializer):
        rel = self.rel

        if rel:
            obj = serializer.save()
            rel.add(obj)
        else:
            super(NestedViewSetMixin, self).perform_create(serializer)

    def perform_destroy(self, instance):
        rel = self.rel

        if rel:
            try:
                rel.remove(instance)
            except AttributeError:
                pass

        return super(NestedViewSetMixin, self).perform_destroy(instance)


class register(object):

    # Map: view/viewset -> url/router instance
    _registry = {}

    @classmethod
    def _add_entry(cls, view, route_object):
        cls._registry[view] = route_object

    @classmethod
    def _has_registered(cls, view):
        return view in cls._registry

    @classmethod
    def get_urls(cls):
        urls = []

        for route_object in cls._registry.values():
            try:
                urls += route_object.urls
            except AttributeError:
                urls.append(route_object)

        return urls

    def __init__(self, pattern, *args, **kwargs):
        self._pattern = pattern
        self._args = args
        self._kwargs = kwargs

    def __call__(self, cls):
        assert not self._has_registered(cls), (
            'View %r has already registered.' % cls
        )

        if is_viewset(cls):
            registrant = (self.register_nested_viewset
                          if cls.nested else self.register_viewset)
        elif is_view(cls):
            registrant = self.register_view
        else:
            raise TypeError(
                '`register` should decorate a ViewSet/APIView, '
                'got %r.' % type(cls)
            )

        registrant(cls, self._pattern, *self._args, **self._kwargs)
        return cls

    def register_view(self, view, pattern):
        self._add_entry(
            view,
            url(pattern, view)
        )

    def register_viewset(self, viewset, pattern, base_name=None, routes=None):
        router_class = get_router_class(routes, DefaultRouter, DefaultRouter)
        router = router_class()
        associate_viewset_with_router(viewset, router, pattern, base_name)
        router.register(pattern, viewset, base_name)

        self._add_entry(viewset, router)

    def register_nested_viewset(self, viewset, pattern,
                                parent_viewset, base_name=None, routes=None):
        assert is_viewset(parent_viewset), (
            '`parent_viewset` must be a ViewSet, '
            'got %r.' % parent_viewset
        )

        viewset = type(
            viewset.__name__,
            (NestedViewSetMixin, viewset),
            dict()
        )

        parent_router = self._registry.get(parent_viewset, None)
        parent_pattern, parent_lookup = parent_viewset._route_info

        assert parent_router is not None, (
            '`parent_viewset` %r must be registered '
            'before sub-viewset.' % parent_viewset
        )

        router_class = get_router_class(
            routes, NestedSimpleRouter, NestedSimpleRouter)
        router = router_class(
            parent_router,
            parent_pattern,
            lookup=parent_lookup
        )
        associate_viewset_with_router(viewset, router, pattern, base_name)
        router.register(pattern, viewset, base_name)

        def get_parent_object(self):
            if hasattr(self, '_parent_object'):
                return self._parent_object

            parent_lookup_kwarg = (
                parent_viewset.lookup_url_kwarg or parent_viewset.lookup_field)
            kwargs = {}
            kwargs.update(self.kwargs)
            kwargs[parent_lookup_kwarg] = self.kwargs.get(
                parent_lookup + '_pk')

            parent_viewset_instance = parent_viewset(
                request=self.request,
                args=self.args,
                kwargs=kwargs,
                _ignore_object_permissions=True
            )
            self._parent_object = parent_viewset_instance.get_object()

            return self._parent_object

        viewset.get_parent_object = get_parent_object

        self._add_entry(viewset, router)
