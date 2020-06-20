from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm


@login_required
def user_details(request):
  if request.method == 'POST':
    form = UserUpdateForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, f'Your account has been updated')
      return redirect('user_details')
  else:
    form = UserUpdateForm(instance=request.user)

  context = {
    'title': 'My Account',
    'form': form
  }
  return render(request, 'user/user_details.html', context)


@login_required
def deactivate_account(request):
  if request.method == 'POST':
    user = request.user
    user.is_active = False
    user.save()
    messages.success(request, f'Your account has been deactivated')
    return redirect('gameplay_home')

  context = {
    'title': 'Deactivate Account',
  }
  return render(request, 'user/deactivate_account.html', context)

