import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


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


@database_sync_to_async  # create a chat in db
def create_message(user, chat, message):
    from .models import Message

    message_instance = Message.objects.create(
        chat=chat,
        sender=user,
        body=message,
    )

    return message_instance


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connecting to personal chat")
        print(f"--->", self.scope["url_route"]["kwargs"]["user"])

        # Ensure the user is authenticated
        # if self.scope["user"].is_authenticated:
        #     request_user = self.scope["user"].id
        # else:
        #     await self.close()

        # Extract the chat_user from the URL kwargs
        chat_user = self.scope["url_route"]["kwargs"]["user"]

        # Get a room name using user ids (request_user and chat_user)
        self.room_group_name = chat_user

        # Create or get the chat in the database
        chat = await create_chat(self.room_group_name)

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        # Send the room name to the WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "room_name",
                "room": chat.chat_name,
            },
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        print(f"Connection closed with code {close_code}")

        # Remove the WebSocket from the group when disconnected
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        request_user = self.scope["user"]
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]

        print(body)

        chat_user = self.scope["url_route"]["kwargs"]["user"]

        # Get a room name using user ids
        self.room_group_name = chat_user

        # Get or create the chat in the database
        chat = await create_chat(self.room_group_name)

        print(f"Chat: {chat.chat_name}")

        # Create a message in the database
        # message = await create_message(
        #     request_user,
        #     chat,
        #     body,
        # )

        # Send the new message to the group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         "type": "chat_message",
        #         "message": {
        #             "message_id": str(message.message_id),  # Convert UUID to string
        #             "chat": str(message.chat),  # Convert UUID to string
        #             "sender": str(message.sender.id),  # Convert UUID to string
        #             "body": message.body,
        #             "created_at": message.created_at.strftime(
        #                 "%H:%M:%S / %Y-%m-%d"
        #             ),  # Format datetime if needed
        #         },
        #     },
        # )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": {
                    "body": body,
                },
            },
        )

    async def chat_message(self, event):
        message = event["message"]

        # Convert UUIDs to strings
        message_data = {
            # "message_id": str(message["message_id"]),
            # "chat": str(message["chat"]),
            # "sender": str(message["sender"]),
            "body": message["body"],
            # "created_at": message["created_at"],
        }

        # Send the message to the WebSocket
        await self.send(
            text_data=json.dumps(message_data)  # Send the complete message data
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
