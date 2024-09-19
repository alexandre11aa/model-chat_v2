from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:code>/', consumers.ChatConsumer.as_asgi()),
]
