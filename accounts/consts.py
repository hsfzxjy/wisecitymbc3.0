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

EXPORTS = ['UserType']
