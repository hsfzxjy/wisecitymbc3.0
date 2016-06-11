from enhancements.collections import Enum

from enhancements.shortcuts import _


class FileType(Enum):

    video = 1
    image = 2
    file = 3

    @classmethod
    def get_choices(cls):
        return {
            cls.video: _('video'),
            cls.image: _('image'),
            cls.file: _('file')
        }


EXPORTS = ['FileType']
