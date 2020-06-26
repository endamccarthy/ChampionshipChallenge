from django.shortcuts import redirect, render
from .forms import EntryForm
from django.contrib import messages
from django.forms.models import inlineformset_factory
from .models import Entry, Prediction, Fixture
from .forms import PredictionForm, FinalistForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory


def home(request):
  context = {
    'title': 'Championship Challenge - Home'
  }
  return render(request, 'gameplay/home.html', context)


def entry(request):

  if request.method == 'POST':
    print(request.POST)

  # round_fixtures = Fixture.objects.all().exclude(
  #   Q(fixture_round='Q') | Q(fixture_round='S') | Q(fixture_round='F') | Q(sport='F')
  # ).order_by('fixture_round')

  fix1 = PredictionForm(initial={'fixture': Fixture.objects.all().first()}, prefix='fix 1')
  fix2 = PredictionForm(prefix='fix 2')

  context = {
    'fix1': fix1,
    'fix2': fix2,
    'title': 'Create Entry'
  }
  return render(request, 'gameplay/entry.html', context)


def error_page(request):
  context = {
    'title': 'Error'
  }
  return render(request, 'gameplay/error_page.html', context)