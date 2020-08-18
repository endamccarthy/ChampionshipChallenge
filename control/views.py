
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from gameplay.models import Fixture, Region
from gameplay.utils import (get_all_round_fixtures_not_played,
                            get_single_instance, update_datetime_on_form_before_saving)

from .forms import FixtureForm


@login_required
def control_home(request):
  fixtures_list = get_all_round_fixtures_not_played()

  context = {
      'fixtures': fixtures_list,
      'regions': Region,
      'title': 'Championship Challenge - Control'
  }
  return render(request, 'control/control_home.html', context)


@login_required
def control_add_fixture(request):
  if request.method == 'POST':
    updated_request = update_datetime_on_form_before_saving(request.POST)
    form = FixtureForm(updated_request)
    if form.is_valid():
      form.save()
      messages.success(request, 'Fixture has been added')
      return redirect('control_home')
  else:
    form = FixtureForm()

  context = {
      'form': form,
      'title': 'Championship Challenge - Add Fixture'
  }
  return render(request, 'control/control_fixture_form.html', context)


@login_required
def control_edit_fixture(request, fixture_id):
  fixture = get_single_instance(Fixture, fixture_id)
  if request.method == 'POST':
    updated_request = update_datetime_on_form_before_saving(request.POST)
    form = FixtureForm(updated_request, instance=fixture)
    if form.is_valid():
      form.save()
      messages.success(request, 'Fixture has been updated')
      return redirect('control_home')
  else:
    form = FixtureForm(instance=fixture)

  context = {
      'form': form,
      'title': 'Championship Challenge - Edit Fixture'
  }
  return render(request, 'control/control_fixture_form.html', context)
