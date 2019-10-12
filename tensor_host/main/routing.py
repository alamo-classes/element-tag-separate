"""
Main channel routing module for Django Channels
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from main.consumers import CaptureLogging

APPLICATION = ProtocolTypeRouter({
    # Capture/Sorter Application Logging Websocket
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path('ws/base/', CaptureLogging)
            ]
        )
    )
})
