from django.db import models

from .base import create_revision_model

from enhancements.shortcuts import _


class Comment(models.Model):

    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    content = models.TextField(_('content'))

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

Stock, StockLog = create_revision_model(
    'Stock',
    dict(
        name=models.CharField(_('name'), max_length=255),
        price=models.FloatField(_('price')),
        volume=models.FloatField(_('volume')),
        company_info=models.TextField(_('company info')),
        comments=models.ManyToManyField(
            Comment, verbose_name=_('brokerage comments'), blank=True)
    ),
    ['price', 'volume'],
    __name__,
    meta=type('Meta', (), {
        'verbose_name': _('stock'),
        'verbose_name_plural': _('stocks')
    })
)

Bond, BondLog = create_revision_model(
    'Bond',
    dict(
        issuer=models.CharField(_('issuer'), max_length=255),
        name=models.CharField(_('name'), max_length=255),
        quantity=models.FloatField(_('quantity')),
        price=models.FloatField(_('price'))
    ),
    ['price', 'quantity'],
    __name__,
    meta=type('Meta', (), {
        'verbose_name': _('bond'),
        'verbose_name_plural': _('bonds')
    })
)

Futures, FuturesLog = create_revision_model(
    'Futures',
    dict(
        name=models.CharField(_('name'), max_length=255),
        price=models.FloatField(_('price'))
    ),
    ['price'],
    __name__,
    meta=type('Meta', (), {
        'verbose_name': _('futures'),
        'verbose_name_plural': _('futures')
    })
)

RawMaterials, RawMaterialsLog = create_revision_model(
    'RawMaterials',
    dict(
        name=models.CharField(_('name'), max_length=255),
        description=models.TextField(_('description')),
        mining_costs=models.FloatField(_('mining costs')),
        processing_costs=models.FloatField(_('processing costs')),
        price=models.FloatField(_('costs'))
    ),
    ['price'],
    __name__,
    meta=type('Meta', (), {
        'verbose_name': _('raw materials'),
        'verbose_name_plural': _('raw materials'),
    })
)
