from services.websocket_consumer import WebsocketConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.urls import path

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path("ws/chat_socket", WebsocketConsumer),
        ])
    ),
})
