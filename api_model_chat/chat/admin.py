from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ('sender', 'receiver', 'message', 'timestamp')

    search_fields = ('sender__name', 'receiver__name', 'message')

    list_filter = ('timestamp', 'sender', 'receiver')

    ordering = ('-timestamp',)

    list_per_page = 20
