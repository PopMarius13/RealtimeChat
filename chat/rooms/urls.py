from django.urls import path
from . import views

urlpatterns = [
  path('', views.all_rooms, name='all_rooms'),
  path('enter_room', views.enter_room, name="enter_room"),
  path('room/<str:room>', views.room, name="room"),
]
