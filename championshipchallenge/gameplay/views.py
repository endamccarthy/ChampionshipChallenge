import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
# from django.forms.models import inlineformset_factory
# from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# from .forms import EntryForm, FinalistForm, PredictionForm
from .models import Entry, Fixture, Prediction, PredictionOption, Team

stripe.api_key = settings.STRIPE_SECRET_KEY


def home_page(request):
  context = {
      'title': 'Championship Challenge - Home'
  }
  return render(request, 'gameplay/home.html', context)


def leaderboard_page(request):
  entries = Entry.objects.all().order_by('-points')
  context = {
      'entries': entries,
      'title': 'Leaderboard'
  }
  return render(request, 'gameplay/leaderboard.html', context)


def fixtures_page(request):
  fixture_list = Fixture.objects.all().exclude(
      Q(fixture_round='Q') | Q(fixture_round='S') | Q(
          fixture_round='F') | Q(sport='F')
  ).order_by('fixture_round')

  context = {
      'fixtures': fixture_list,
      'title': 'Fixtures'
  }
  return render(request, 'gameplay/fixtures.html', context)


@login_required
def create_entry_page(request):
  provincial_round_fixtures = Fixture.objects.all().exclude(
      Q(fixture_round='Q') | Q(fixture_round='S') | Q(
          fixture_round='F') | Q(sport='F')
  ).order_by('fixture_round')

  if request.method == 'POST':
    new_entry = Entry.objects.create(user=request.user)
    for key, value in request.POST.items():
      fixture_id = None
      if "fixture_prediction" in key:
        fixture_id = [int(id) for id in key.split('_') if id.isdigit()][0]
        prediction_id, created = Prediction.objects.get_or_create(
            fixture=Fixture.objects.get(id=fixture_id), prediction=value)
        if created:
          new_entry.predictions.add(prediction_id)
        continue
    return redirect('gameplay_review_entry', entry_id=new_entry.id)
  context = {
      'provincial_round_fixtures': provincial_round_fixtures,
      'prediction_options': PredictionOption,
      'team_options': Team.objects.all(),
      'title': 'Create Entry'
  }
  return render(request, 'gameplay/create_entry.html', context)


@login_required
@csrf_exempt
def checkout_page(request):
  product_price = stripe.Price.retrieve('price_1H4ocuKSkIdC4LCMnGWYJwGx')
  session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items=[{
          'price': product_price,
          'quantity': 1,
      }],
      mode='payment',
      success_url=request.build_absolute_uri(
          reverse('gameplay_home')) + '?session_id={CHECKOUT_SESSION_ID}',
      cancel_url=request.build_absolute_uri(reverse('gameplay_create_entry')),
  )
  return JsonResponse({
      'session_id': session.id,
      'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY
  })


# @login_required
# @csrf_exempt
# def stripe_webhook(request):
#   # You can find your endpoint's secret in your webhook settings
#   endpoint_secret = 'whsec_gLJRXaEEV0BbTXQqfuIRC5Hiqz63hOQ1'

#   payload = request.body
#   sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#   event = None

#   try:
#     event = stripe.Webhook.construct_event(
#         payload, sig_header, endpoint_secret
#     )
#   except ValueError as e:
#     # Invalid payload
#     return HttpResponse(status=400)
#   except stripe.error.SignatureVerificationError as e:
#     # Invalid signature
#     return HttpResponse(status=400)

#   # Handle the checkout.session.completed event
#   if event['type'] == 'checkout.session.completed':
#     session = event['data']['object']
#     print(session)
#     # try:
#     #   entry = Entry.objects.get(pk=entry_id)
#     #   entry.paid = True
#     #   entry.save()
#     #   messages.success(request, 'Your payment was received!')
#     #   return redirect('gameplay_entry', entry_id=entry_id)
#     # except AttributeError:
#     #   return redirect('gameplay_error_page')

#   return HttpResponse(status=200)


def entry_page(request, entry_id):
  entry = get_single_entry(entry_id)
  context = {
      'entry': entry,
      'title': 'Entry'
  }
  return render(request, 'gameplay/entry.html', context)


def get_single_entry(entry_id):
  try:
    entry = Entry.objects.get(id=entry_id)
    return entry
  except Entry.DoesNotExist:
    return redirect('gameplay_error_page')


def user_entries_page(request):
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
