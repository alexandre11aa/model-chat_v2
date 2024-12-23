from django.contrib import admin

from attachments.models import FileAttachment, AudioAttachment

admin.site.register(FileAttachment)
admin.site.register(AudioAttachment)
