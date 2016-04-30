from enum import Enum, unique

EXPORTS = ['TYPES', 'UserType']

TYPES = {
    'Government': 'Government'
}


@unique
class UserType(Enum):
    Gov = 1
    Com = 2
    Chr = 3
