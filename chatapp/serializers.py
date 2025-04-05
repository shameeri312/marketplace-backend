from rest_framework import serializers
from .models import *

# serializers.py


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["chat_id", "chat_name"]


class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%H:%M:%S / %Y-%m-%d")
    chat = serializers.CharField(source="chat.chat_name", read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "chat",
            "sender",
            "body",
            "created_at",
        ]
