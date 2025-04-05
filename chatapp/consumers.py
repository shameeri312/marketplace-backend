import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs, unquote
from django.contrib.auth import get_user_model

User = get_user_model()  # Use your custom UserAccount model if different


def get_room_name(user1_id, user2_id):
    user1_id_str = str(user1_id)
    user2_id_str = str(user2_id)
    sorted_ids = sorted([user1_id_str, user2_id_str])
    room_name = f"chat_{sorted_ids[0]}_{sorted_ids[1]}"

    return room_name


@database_sync_to_async
def create_chat(room_name):
    from .models import Chat

    chat, created = Chat.objects.get_or_create(chat_name=room_name)

    return chat


@database_sync_to_async
def create_message(user, chat, message):
    from .models import Message

    message_instance = Message.objects.create(
        chat=chat,
        sender=user,  # Full user instance
        body=message,
    )

    return message_instance


@database_sync_to_async
def get_user_by_id(user_id):
    return User.objects.get(id=user_id)  # Fetch user by ID


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connecting to personal chat")
        print(f"--->", self.scope["url_route"]["kwargs"]["user"])

        # Extract the chat_user from the URL kwargs
        chat_user = self.scope["url_route"]["kwargs"]["user"]

        # Get query parameters
        query_string = self.scope["query_string"].decode("utf-8")
        query_params = parse_qs(query_string)
        self.user_id = query_params.get("user_id", [None])[0]

        if not self.user_id:
            print("No user_id provided in query parameters")
            await self.close()
            return

        print(f"User ID from query: {self.user_id}")

        # Validate user_id against authenticated user
        if not self.scope.get("user") or not hasattr(self.scope["user"], "id"):
            print("User not authenticated")
            await self.close()
            return

        authenticated_user_id = str(self.scope["user"].id)
        if self.user_id != authenticated_user_id:
            print(
                f"User ID mismatch: query ({self.user_id}) vs authenticated ({authenticated_user_id})"
            )
            await self.close()
            return

        # Set the room group name using both user IDs
        self.room_group_name = chat_user

        # Create or get the chat in the database
        chat = await create_chat(self.room_group_name)

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Send the room name to the WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "room_name",
                "user": self.user_id,
                "room": chat.chat_name,
            },
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f"Connection closed with code {close_code}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        user = self.scope["user"]  # Full user instance
        print("---> ", user)

        text_data_json = json.loads(text_data)
        body = text_data_json["body"]
        chat_user = self.scope["url_route"]["kwargs"]["user"]
        self.room_group_name = chat_user

        chat = await create_chat(self.room_group_name)

        message = await create_message(user, chat, body)

        print("---> Message: %s" % message)

        # Broadcast to others only
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": {
                    "body": body,
                    "userId": str(user.id),
                    "message_id": str(message.message_id),
                    "sender": user.id,
                    "created_at": message.created_at.strftime(
                        "%H:%M:%S / %Y-%m-%d"
                    ),  # Format datetime if needed
                },
            },
        )

    async def chat_message(self, event):
        message_data = event["message"]
        await self.send(
            text_data=json.dumps(
                {
                    "body": message_data["body"],
                    "userId": message_data["userId"],
                    "message_id": message_data["message_id"],
                    "sender": message_data["sender"],
                    "created_at": message_data["created_at"],
                }
            )
        )

    async def room_name(self, event):
        room_name = event["room"]
        await self.send(
            text_data=json.dumps(
                {
                    "room": room_name,
                }
            )
        )
