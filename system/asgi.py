import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chatapp.middleware import QueryAuthMiddleware
from chatapp.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
print("ASGI application loaded")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": QueryAuthMiddleware(
            URLRouter(websocket_urlpatterns),
        ),
    }
)
