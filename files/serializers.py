from enhancements.rest import serializers

from .models import File


@serializers.register(File)
class FileSerializer(serializers.ModelSerializer):
    pass
