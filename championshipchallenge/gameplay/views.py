from django.shortcuts import redirect, render
from .forms import EntryForm
from django.contrib import messages
from django.forms.models import inlineformset_factory
from .models import Entry, Fixture, PredictionOption, Prediction, Team, Finalist
from .forms import PredictionForm, FinalistForm
from django.db.models import Q
from django.http import HttpResponseRedirect


def home(request):
  context = {
    'title': 'Championship Challenge - Home'
  }
  return render(request, 'gameplay/home.html', context)


def entry(request):

  provincial_round_fixtures = Fixture.objects.all().exclude(
    Q(fixture_round='Q') | Q(fixture_round='S') | Q(fixture_round='F') | Q(sport='F')
  ).order_by('fixture_round')

  provincial_final_fixtures = Fixture.objects.filter(fixture_round='F').exclude(region='A')

  if request.method == 'POST':

    new_entry = Entry.objects.create(user=request.user)

    for key, value in request.POST.items():
      fixture_id = None
      winner_id = None
      runner_up_id = None
      if "fixture_prediction" in key:
        fixture_id = [int(id) for id in key.split('_') if id.isdigit()][0]
        temp, created = Prediction.objects.get_or_create(fixture=Fixture.objects.get(id=fixture_id), prediction=value)
        new_entry.predictions.add(temp)
        continue


    # messages.success(request, 'Your account has been updated!')
    # return redirect('profile')

  context = {
    'provincial_round_fixtures': provincial_round_fixtures,
    'provincial_final_fixtures': provincial_final_fixtures,
    'prediction_options': PredictionOption,
    'team_options': Team.objects.all(),
    'title': 'Create Entry'
  }
  return render(request, 'gameplay/entry.html', context)


def error_page(request):
  context = {
    'title': 'Error'
  }
  return render(request, 'gameplay/error_page.html', context)