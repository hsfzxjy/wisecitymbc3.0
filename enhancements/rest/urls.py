from rest_framework.routers import DefaultRouter, BaseRouter

from .routers import custom_router

_default_router = DefaultRouter()
_routers = [_default_router]


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

        return viewset_class


def generate_urls():
    urls = []
    for router in _routers:
        urls += router.urls

    return urls
