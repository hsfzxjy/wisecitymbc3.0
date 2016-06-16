from rest_framework import serializers

from enhancements.rest import registry

from .models import File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File

registry.register(File, FileSerializer)
