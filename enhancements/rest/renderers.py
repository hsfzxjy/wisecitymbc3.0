from rest_framework import renderers

from json import JSONEncoder

from enhancements.collections import Enum


class EnumJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value

        return super(EnumJSONEncoder, self).default(obj)


class JSONRenderer(renderers.JSONRenderer):

    encoder_class = EnumJSONEncoder
