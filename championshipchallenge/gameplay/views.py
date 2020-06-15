from django.shortcuts import render
# from django.contrib import messages


def home(request):
  context = {
    'title': 'Championship Challenge - Home'
  }
  return render(request, 'gameplay/home.html', context)


def error_page(request):
  context = {
    'title': 'Error'
  }
  return render(request, 'gameplay/error_page.html', context)