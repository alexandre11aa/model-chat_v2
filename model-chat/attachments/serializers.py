from rest_framework import serializers

from attachments.models import FileAttachment, AudioAttachment
from attachments.utils.formatter import Formatter

from django.conf import settings


class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachment
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['size'] = Formatter.format_bytes(instance.size)
        data['src'] = f'{settings.CURRENT_URL}{instance.src}'

        return data


class AudioAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioAttachment
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['src'] = f'{settings.CURRENT_URL}{instance.src}'

        return data