from enum import Enum

from enhancements.constants.utils import annotate
from enhancements.shortcuts import _


class FileType(Enum):

    video = 1
    image = 2
    file = 3

FILE_TYPE_CHOICES = annotate({
    FileType.video: _('video'),
    FileType.image: _('image'),
    FileType.file: _('file')
})

EXPORTS = ['FileType']