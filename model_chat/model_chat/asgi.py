"""
ASGI config for model_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat import routings as chat_routing
from chat_group import routings as chat_group_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'model_chat.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_group_routing.websocket_urlpatterns + chat_routing.websocket_urlpatterns
        )
    ),
})