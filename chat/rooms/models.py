from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Room(models.Model):
  name = models.CharField(max_length=1000)
  users = models.ManyToManyField(User, blank=True)

class Message(models.Model):
  value = models.CharField(max_length=1000000)
  data = models.DateTimeField(default=datetime.now, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  is_image = models.BooleanField(default=False)
  image= models.ImageField(null=True, blank=True, upload_to='images/')


class UserInformation(models.Model):
  email = models.EmailField(max_length=1000)
  is_online = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

