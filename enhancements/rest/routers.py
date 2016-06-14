from rest_framework.routers import BaseRouter, Route


def custom_router(routes, base=BaseRouter):
    return type(
        'CustomRouter',
        (base, ),
        {
            'routes': [Route(**kwargs) for kwargs in routes]
        }
    )
