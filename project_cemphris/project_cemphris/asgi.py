"""
ASGI config for project_cemphris project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_cemphris.settings')

import django
django.setup()

from project_cemphris.urls import websocket_urlpatterns

# application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    # WebSocket chat handler
    'websocket': AllowedHostsOriginValidator(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})