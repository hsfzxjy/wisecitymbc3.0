from enhancements.collections import Enum
from enhancements.shortcuts import _


class UserType(Enum):

    government = 1
    company = 2
    bureau = 3

    @classmethod
    def get_choices(cls):
        return {
            cls.government: _('government'),
            cls.company: _('company'),
            cls.bureau: _('bureau'),
        }


class BureauType(Enum):

    none = 1
    real_estate = 2
    car = 3
    electronic_technology = 4
    bank = 5
    energy_and_raw_materials = 6
    financial_system = 7
    media = 8

    @classmethod
    def get_choices(cls):
        return {
            cls.none: _('none'),
            cls.real_estate: _('real_estate'),
            cls.car: _('car'),
            cls.electronic_technology: _('electronic_technology'),
            cls.bank: _('bank'),
            cls.energy_and_raw_materials: _('energy_and_raw_materials'),
            cls.financial_system: _('financial_system'),
            cls.media: _('media'),
        }

user_type_verbose = UserType.get_choices()
bureau_type_verbose = BureauType.get_choices()

EXPORTS = ['UserType', 'BureauType',
           'user_type_verbose', 'bureau_type_verbose']
