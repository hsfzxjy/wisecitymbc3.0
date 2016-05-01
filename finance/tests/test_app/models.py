from django.db import models

from base import create_revision_model

Stock, StockLog = create_revision_model(
    'Stock',
    dict(price=models.FloatField()),
    ['price'],
    __name__,
    meta=type('Meta', (), {
        'verbose_name': 'Stock'
    })
)
