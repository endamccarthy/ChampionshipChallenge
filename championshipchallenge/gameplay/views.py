from django.shortcuts import render
from django.contrib import messages


def home(request):
  messages.success(request, 'Your account has been created! You are now able to login')
  context = {
    'title': 'Home'
  }
  return render(request, 'gameplay/home.html', context)