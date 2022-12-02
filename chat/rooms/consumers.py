import json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from datetime import datetime
from django.core.mail import send_mail

from .models import Room, Message, UserInformation

# icoseutfxzqtiasy


class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'chat_{self.room_name}'

    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )
    await self.accept()


  async def disconnect(self, code):
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )


  async def receive(self, text_data):
    data = json.loads(text_data)
    message = data['message']
    username = data['username']
    room = data['room']
    username2 = data['username2']


    await self.save_message(username, room, message)

    await self.send_email(username, message, username2)

    # Send message to room group
    await self.channel_layer.group_send(
      self.room_group_name,
      {
          'type': 'chat_message',
          'message': message,
          'username': username,
          'date': datetime.now().strftime('%Y-%m-%d, %H:%M'),
      }
    )


  # Receive message from room group
  async def chat_message(self, event):
    message = event['message']
    username = event['username']

    # Send message to WebSocket
    await self.send(text_data=json.dumps({
      'message': message,
      'username': username,
      'date': datetime.now().strftime('%b %d,%Y, %I:%M %P')
    }))

  @sync_to_async
  def save_message(self, username, room, message):
    user = User.objects.get(username=username)
    room = Room.objects.get(name=room)

    message = Message.objects.create(user=user, room=room, value=message)
    message.save()

  @sync_to_async
  def send_email(self, username, message, username2):
    user = User.objects.get(username=username)
    user_information = UserInformation.objects.get(user=user)
    user2 = User.objects.get(username=username2)
    user_information2 = UserInformation.objects.get(user=user2)

    if not user_information2.is_online:
      send_mail(
        f'Hi {username2}, you have a new message from {username}!',
        f'{message}',
        f'{user_information.email}',
        [f'{user_information2.email}'],
      )

