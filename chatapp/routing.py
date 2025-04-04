from django.urls import path
from .consumers import PersonalChatConsumer

websocket_urlpatterns = [
    path("ws/chat/<str:user>/", PersonalChatConsumer.as_asgi()),
]
