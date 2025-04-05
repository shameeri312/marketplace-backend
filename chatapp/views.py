from .serializers import *
from .models import *
from rest_framework import viewsets, permissions
from rest_framework import generics

# views.py


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "chat_id"
    http_method_names = ["get", "delete"]  # only allow list and delete


class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Message.objects.all()
        chat_id = self.request.query_params.get("chat", None)

        if chat_id is not None:
            queryset = queryset.filter(chat=chat_id)

        return queryset
