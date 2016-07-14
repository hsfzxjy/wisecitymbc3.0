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

    @classmethod
    def get_by_mime_type(cls, mime_type):
        for type, mime_list in MIME_TYPES.items():
            if [ext for ext in mime_list if ext in mime_type]:
                return type

        return cls.file


EXPORTS = ['FileType']

MIME_TYPES = {
    FileType.video: (
        'aac',
        'mp4',
        'mpeg',
        'ogg',
        'wav',
        'webm',
    ),
    FileType.image: (
        'png',
        'jpg',
        'bmp',
        'gif',
        'jpeg',
        'tiff',
        'x-xbitmap',
    )
}
