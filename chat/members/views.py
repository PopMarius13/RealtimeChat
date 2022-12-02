from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from rooms.models import UserInformation


def login_user(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      if not UserInformation.objects.filter(user_id=user.id).exists():
        UserInformation.objects.create(is_online=True, user=user)
      else:
        user_information = UserInformation.objects.get(user_id=user.id)
        user_information.is_online = True
        user_information.save()
      login(request, user)
      return redirect('home')
    else:
      messages.success(request, "The username or password you entered is incorrect!!!")
      return redirect('login')
  else:
    return render(request, 'authenticate/login.html', {})

def logout_user(request):
  user_information = UserInformation.objects.get(user_id=request.user.id)
  user_information.is_online = False
  user_information.save()
  logout(request)
  messages.success(request, "Bye Bye!")
  return redirect('home')

def register_user(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      if not UserInformation.objects.filter(user_id=user.id).exists():
        UserInformation.objects.create(is_online=True, user=user)
      else:
        user_information = UserInformation.objects.get(user_id=user.id)
        user_information.is_online = True
        user_information.save()
      login(request, user)
      messages.success(request, ("Registration Successful!"))
      return redirect('home')
  else:
    form = UserCreationForm()

  return render(request, "authenticate/register_user.html", {
    'form': form
  })

def home(request):
  user_information = "empty"
  if request.user.id:
    user_information = UserInformation.objects.get(user_id=request.user.id)
  return render(request, 'authenticate/home.html', {
    'user_information': user_information
  })

def change_email(request):
  email = request.POST['email']
  if email:
    user_information = UserInformation.objects.get(user_id= request.user.id)
    user_information.email = email
    user_information.save()
    messages.success(request, ("You have a new email!"))
  return redirect('home')

