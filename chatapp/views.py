from .serializers import *
from .models import Message
from rest_framework import viewsets, permissions


class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Message.objects.all()
        chat_id = self.request.query_params.get("chat", None)

        if chat_id is not None:
            queryset = queryset.filter(chat=chat_id)

        return queryset
