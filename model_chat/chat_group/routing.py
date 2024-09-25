from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/group/<int:group_chat_id>/', consumers.GroupChatConsumer.as_asgi()),
]