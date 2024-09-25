from django.contrib import admin
from .models import GroupChat, GroupMessage

@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Exibir o nome do grupo
    search_fields = ('name',)  # Permitir busca pelo nome do grupo
    ordering = ('name',)  # Ordenar por nome
    list_per_page = 20  # Limitar por página

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'group_chat', 'message', 'timestamp')  # Exibir o remetente, grupo, mensagem e timestamp
    search_fields = ('sender__name', 'group_chat__name', 'message')  # Permitir busca por nome do remetente, grupo e mensagem
    list_filter = ('timestamp', 'sender', 'group_chat')  # Filtrar por timestamp, remetente e grupo
    ordering = ('-timestamp',)  # Ordenar por timestamp decrescente
    list_per_page = 20  # Limitar por página