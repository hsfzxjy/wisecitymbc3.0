from enhancements.collections import Enum

from enhancements.shortcuts import _

from accounts.consts import BureauType, UserType


EXPORTS = ['ArticleType', 'article_type_verbose']


class ArticleType(Enum):

    company = 1
    government = 2
    media = 3
    finance = 4
    energy_and_raw_materials = 5
    electronic_technology = 6
    bank = 7
    real_estate = 8

    @classmethod
    def from_user(cls, user):
        return USER_TO_ARTICLE_MAPPING.get(
            (user.user_type, user.bureau_type), None)

    @classmethod
    def get_choices(cls):
        return {
            cls.company: _('company'),
            cls.government: _('government'),
            cls.media: _('media'),
            cls.finance: _('finance'),
            cls.energy_and_raw_materials: _('energy_and_raw_materials'),
            cls.electronic_technology: _('electronic_technology'),
            cls.bank: _('bank'),
            cls.real_estate: _('real_estate')
        }

USER_TO_ARTICLE_MAPPING = {
    (UserType.company, BureauType.none): ArticleType.company,
    (UserType.government, BureauType.none): ArticleType.government,
    (UserType.bureau, BureauType.media): ArticleType.media,
    (UserType.bureau, BureauType.financial_system): ArticleType.finance,
    (UserType.bureau, BureauType.energy_and_raw_materials):
    ArticleType.energy_and_raw_materials,
    (UserType.bureau, BureauType.car): ArticleType.government,
    (UserType.bureau, BureauType.electronic_technology):
    ArticleType.electronic_technology,
    (UserType.bureau, BureauType.real_estate): ArticleType.real_estate,
    (UserType.bureau, BureauType.bank): ArticleType.bank
}

article_type_verbose = ArticleType.get_choices()
