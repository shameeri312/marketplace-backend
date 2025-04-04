import uuid
from django.db import models
from users.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Chat(models.Model):
    chat_id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
    )
    chat_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.chat_name)


class Message(models.Model):
    message_id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
    )
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender}: {self.body[0:10]}"
