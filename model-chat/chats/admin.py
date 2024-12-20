from django.contrib import admin

from chats.models import Chat, ChatMessage

admin.site.register(Chat)
admin.site.register(ChatMessage)