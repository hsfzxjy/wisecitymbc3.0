from rest_framework.routers import BaseRouter, Route


def custom_router(routes):
    return type(
        'CustomRouter',
        (BaseRouter, ),
        {
            'routes': [Route(**kwargs) for kwargs in routes]
        }
    )
