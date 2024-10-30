import json

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_tether.settings')  # Replace with your actual project name
django.setup()

from channels.generic.websocket import AsyncWebsocketConsumer
from base.models import Message, Room,User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room groups
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope["user"].username  # If using auth
        room = self.room_name
        userid = self.scope["user"].id
        # Save message to database (optional)
        # Add code here to save 'message' to your Message model in the database
        await self.save_message(username,room,message)
        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "userid":userid
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        userid = event['userid']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "userid":userid
        }))
    
    @sync_to_async
    def save_message(self,username,room_name,message):
        user = User.objects.get(username=username)
        room = Room.objects.get(id=room_name)
        Message.objects.create(user=user,room=room,body=message)