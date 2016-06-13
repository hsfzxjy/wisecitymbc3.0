from enhancements.collections import Enum

from enhancements.shortcuts import _

from accounts.consts import BureauType, UserType


EXPORTS = ['ArticleType']


class ArticleType(Enum):

    company = 1
    government = 2
    media = 3
    finance = 4
    energy_and_raw_materials = 5

    def from_user(self, user):
        return USER_TO_ARTICLE_MAPPING[(user.user_type, user.bureau_type)]

    @classmethod
    def get_choices(cls):
        return {
            cls.company: _('company'),
            cls.government: _('government'),
            cls.media: _('media'),
            cls.finance: _('finance'),
            cls.energy_and_raw_materials: _('energy_and_raw_materials'),
        }

USER_TO_ARTICLE_MAPPING = {
    (UserType.company, BureauType.none): ArticleType.company,
    (UserType.government, BureauType.none): ArticleType.government,
    (UserType.bureau, BureauType.media): ArticleType.media,
    (UserType.bureau, BureauType.financial_system): ArticleType.finance,
    (UserType.bureau, BureauType.enegry_and_raw_materials):
    ArticleType.government,
    (UserType.bureau, BureauType.car): ArticleType.government,
    (UserType.bureau, BureauType.electronic_technology):
    ArticleType.government,
    (UserType.bureau, BureauType.real_estate): ArticleType.government,
    (UserType.bureau, BureauType.bank): ArticleType.government
}
