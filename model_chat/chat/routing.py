from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:user1_code>/<str:user2_code>/', consumers.ChatConsumer.as_asgi()),
]