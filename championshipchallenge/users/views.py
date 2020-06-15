from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.contrib import messages


@login_required
def account(request):
  context = {
    'title': 'My Account',
  }
  return render(request, 'users/account.html', context)

