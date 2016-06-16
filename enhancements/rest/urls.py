from rest_framework.routers import DefaultRouter, BaseRouter
from rest_framework_nested.routers import NestedSimpleRouter

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from django.conf.urls import url

from .routers import custom_router

_default_router = DefaultRouter()
_routers = [_default_router]
_router_map = {}

_urls = []


def _get_key(viewset):
    return '.'.join((viewset.__module__, viewset.__class__.__name__))


def _store_viewset(viewset, router):
    _router_map[_get_key(viewset)] = router


def _get_router(viewset):
    try:
        return _router_map[_get_key(viewset)]
    except KeyError:
        raise ValueError("Viewset %r hasn't been registered." % viewset)


class register_nested(object):

    def __init__(self, prefix, required, parent_prefix,
                 lookup=None, base_name=None, routes=None):
        self.prefix, self.parent_prefix, self.base_name = prefix, \
            parent_prefix, base_name

        self.parent_router = _get_router(required)

        if routes is not None:
            router_class = custom_router(routes, NestedSimpleRouter)
        else:
            router_class = NestedSimpleRouter

        self.router = router_class(self.parent_router,
                                   parent_prefix, lookup=lookup)
        _routers.append(self.router)

    def __call__(self, viewset_class):
        self.router.register(self.prefix, viewset_class, self.base_name)
        _store_viewset(viewset_class, self.router)

        return viewset_class


class register(object):

    def __init__(self, prefix, base_name=None, router=None):
        self._prefix, self._base_name = prefix, base_name

        if router is None:
            # default
            self._router = _default_router
        elif isinstance(router, dict):
            # Custom routes
            self._router = custom_router(router)
            _routers.append(self._router)
        else:
            assert isinstance(router, BaseRouter), \
                "Custom router must be instance of `BaseRouter`, "\
                "got %r." % type(router)

            self._router = router

            # Check if registered
            if not hasattr(router, '_registered'):
                router._registered = True
                _routers.append(router)

    def __call__(self, viewset_class):
        self._router.register(
            self._prefix,
            viewset_class,
            self._base_name
        )

        _store_viewset(viewset_class, self._router)

        return viewset_class


class register_view(object):

    def __init__(self, prefix):
        self._prefix = prefix

    def __call__(self, view):
        _urls.append(url(self._prefix, view.as_view()))

        return view


def generate_urls():
    urls = []
    for router in _routers:
        urls += router.urls

    return urls + _urls
