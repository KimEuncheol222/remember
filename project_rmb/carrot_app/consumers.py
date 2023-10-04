import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import ChatRoom, ChatMessage
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Load previous messages and send them to the client
        await self.load_previous_messages()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        # Save the message to the database
        await self.save_message(username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username
            }
        )

    @database_sync_to_async
    def save_message(self, username, message):
        user = User.objects.get(username=username)
        chat_room = ChatRoom.objects.get(id=self.room_name)

        ChatMessage.objects.create(
            chat_room=chat_room,
            sender=user,
            message=message
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))

    @database_sync_to_async
    async def load_previous_messages(self):
        chat_room = ChatRoom.objects.get(id=self.room_name)
        messages = ChatMessage.objects.filter(chat_room=chat_room)
        for message in messages:
            await self.send(text_data=json.dumps({
                "message": message.message,
                "username": message.sender.username
            }))