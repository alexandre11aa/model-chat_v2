from django.urls import path
from .views import create_group_chat, group_chat_view, groups_list

urlpatterns = [
    path("chat/group/create/", create_group_chat, name="create_group_chat"),
    path('chat/group/list-groups/', groups_list, name='groups_list'),
    path("chat/group/<int:group_chat_id>/", group_chat_view, name="group_chat"),
]