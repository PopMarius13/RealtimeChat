from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rooms.models import Room, Message, UserInformation
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def all_rooms(request):
  users = User.objects.all()
  current_user = request.user.username
  return render(request, 'rooms/rooms.html', {
    'users': users,
    'current_user': current_user
  })

@login_required
def enter_room(request):
  username1 = request.user.username
  username2 = request.POST['username']
  if username1 > username2:
    first_name = username1
    second_name = username2
  else:
    first_name = username2
    second_name = username1
  roomName = f"{first_name}-{second_name}"

  if not Room.objects.filter(name=roomName).exists():
    new_room = Room.objects.create(name=roomName)
    new_room.users.add(User.objects.get(username=first_name))
    new_room.users.add(User.objects.get(username=second_name))
    new_room.save()
  return redirect(f'room/{roomName}')

@login_required
def room(request, room):
  current_room = Room.objects.get(name=room)
  user1 = current_room.users.all()[0]
  user2 = current_room.users.all()[1]
  messages = Message.objects.filter(room=current_room)

  if user1.username != request.user.username:
    user1, user2 = user2, user1

  return render(request, 'rooms/room.html', {
    'room': current_room,
    'user1': user1,
    'user2': user2,
    'room_messages': messages
  })

