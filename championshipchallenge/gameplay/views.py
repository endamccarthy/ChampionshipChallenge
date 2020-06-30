from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.db.models import Q
from django.http import HttpResponseRedirect
from .models import Entry, Fixture, PredictionOption, Prediction, Team, Finalist
from .forms import EntryForm, PredictionForm, FinalistForm

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
  context = {
    'title': 'Championship Challenge - Home'
  }
  return render(request, 'gameplay/home.html', context)


def leaderboard(request):
  entries = Entry.objects.all().order_by('-points')
  context = {
    'entries': entries,
    'title': 'Leaderboard'
  }
  return render(request, 'gameplay/leaderboard.html', context)


def fixtures(request):
  fixtures = Fixture.objects.all().exclude(
    Q(fixture_round='Q') | Q(fixture_round='S') | Q(fixture_round='F') | Q(sport='F')
  ).order_by('fixture_round')
  
  context = {
    'fixtures': fixtures,
    'title': 'Fixtures'
  }
  return render(request, 'gameplay/fixtures.html', context)


@login_required
def create_entry(request):
  provincial_round_fixtures = Fixture.objects.all().exclude(
    Q(fixture_round='Q') | Q(fixture_round='S') | Q(fixture_round='F') | Q(sport='F')
  ).order_by('fixture_round')

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
    return redirect('gameplay_checkout', entry_id=new_entry.id)

  context = {
    'provincial_round_fixtures': provincial_round_fixtures,
    'prediction_options': PredictionOption,
    'team_options': Team.objects.all(),
    'title': 'Create Entry'
  }
  return render(request, 'gameplay/create_entry.html', context)


@login_required
def checkout(request, entry_id):
  if request.method == 'POST':
    try:
      email = request.user.email
      name = request.user.get_full_name()
      customer = stripe.Customer.create(
        email=email,
        name=name,
        source=request.POST['stripeToken']
      )
      charge = stripe.Charge.create(
        customer=customer,
        amount=1000,
        currency='eur',
        description="Entry Fee"
      )
      entry = Entry.objects.get(pk=entry_id)
      entry.paid = True
      entry.save()
      messages.success(request, 'Your payment was received!')
      return redirect('gameplay_entry', entry_id=entry_id)
    except AttributeError:
      return redirect('gameplay_error_page')

  context = {
    'title': 'Checkout'
  }
  return render(request, 'gameplay/checkout.html', context)


def entry(request, entry_id):
  try:
    entry = Entry.objects.get(id=entry_id)
  except Entry.DoesNotExist:
    return redirect('gameplay_error_page')
  
  context = {
    'entry': entry,
    'title': 'Entry'
  }
  return render(request, 'gameplay/entry.html', context)


def user_entries(request):
  entries = Entry.objects.filter(user=request.user).order_by('-points')
  context = {
    'entries': entries,
    'title': 'My Entries'
  }
  return render(request, 'gameplay/user_entries.html', context)


def error_page(request):
  context = {
    'title': 'Error'
  }
  return render(request, 'gameplay/error_page.html', context)