from django.contrib import admin

from accounts.admin import all_objects

from chats.models import Chat, ChatMessage

admin.site.register(Chat, all_objects)
admin.site.register(ChatMessage, all_objects)