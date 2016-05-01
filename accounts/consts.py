from enum import Enum

from enhancements.constants.utils import annotate
from enhancements.shortcuts import _


class UserType(Enum):

    government = 1
    company = 2
    bureau = 3

USER_TYPE_CHOICES = annotate({
    UserType.government: _('government'),
    UserType.company: _('company'),
    UserType.bureau: _('bureau'),
})


class BureauType(Enum):

    none = 1
    real_estate = 2
    car = 3
    electronic_technology = 4
    bank = 5
    enegry_and_raw_materials = 6
    financial_system = 7
    media = 8

BUREAU_TYPE_CHOICES = annotate({
    BureauType.none: _('none'),
    BureauType.real_estate: _('real_estate'),
    BureauType.car: _('car'),
    BureauType.electronic_technology: _('electronic_technology'),
    BureauType.bank: _('bank'),
    BureauType.enegry_and_raw_materials: _('enegry_and_raw_materials'),
    BureauType.financial_system: _('financial_system'),
    BureauType.media: _('media'),
})

EXPORTS = ['UserType', 'BureauType']
