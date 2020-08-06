import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render

from .models import Entry, Fixture, Prediction, PredictionOption
from .utils import get_single_entry, get_all_round_hurling_fixtures

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
  return render(request, 'gameplay/entry_list.html', context)


def fixtures_page(request):
  fixture_list = get_all_round_hurling_fixtures()

  context = {
      'fixtures': fixture_list,
      'title': 'Fixtures'
  }
  return render(request, 'gameplay/fixtures.html', context)


@login_required
def create_entry_page(request):
  provincial_round_fixtures = get_all_round_hurling_fixtures()

  if request.method == 'POST':
    new_entry = Entry.objects.create(user=request.user)
    for key, value in request.POST.items():
      fixture_id = None
      if 'fixture_prediction' in key:
        fixture_id = [int(id) for id in key.split('_') if id.isdigit()][0]
        prediction, created = Prediction.objects.get_or_create(
            fixture=Fixture.objects.get(id=fixture_id), prediction=value)
        if prediction:
          new_entry.predictions.add(prediction)
        continue
    messages.success(request, 'Your entry has been submitted!')
    return redirect('gameplay_entry', entry_id=new_entry.id)

  context = {
      'provincial_round_fixtures': provincial_round_fixtures,
      'prediction_options': PredictionOption,
      'title': 'Create Entry'
  }
  return render(request, 'gameplay/create_entry.html', context)


"""
@login_required
def checkout_page(request, entry_id):
  context = {
      'entry_id': entry_id,
      'public_key': settings.STRIPE_PUBLISHABLE_KEY,
      'title': 'Checkout'
  }
  return render(request, 'gameplay/checkout.html', context)


@login_required
@csrf_exempt
def checkout(request, entry_id):
  try:
    # a product is set up on my stripe dashboard
    product_price = stripe.Price.retrieve(
        settings.STRIPE_PRODUCT_SINGLE_ENTRY_PRICE_ID)
    # retrieve existing customer from stripe or create new one
    customer_list = stripe.Customer.list(
        email=request.user.email, limit=1)['data']
    if not customer_list:
      customer = stripe.Customer.create(email=request.user.email)
    else:
      customer = customer_list[0]
    # create a new stripe payment intent
    intent = stripe.PaymentIntent.create(
        amount=product_price['unit_amount'],
        currency=product_price['currency'],
        customer=customer,
        # this might be needed if using a webhook to confirm the entry has been paid
        metadata={
            'entry_id': entry_id,
        }
    )

    return JsonResponse({
        'clientSecret': intent['client_secret'],
    })

  except stripe.error.CardError as e:
    body = e.json_body
    err = body.get('error', {})
    messages.warning(request, f"{err.get('message')}")

  except stripe.error.RateLimitError as e:
    # Too many requests made to the API too quickly
    messages.warning(request, "Rate limit error")

  except stripe.error.InvalidRequestError as e:
    messages.warning(request, "Invalid parameters")

  except stripe.error.AuthenticationError as e:
    # Authentication with Stripe's API failed
    # (maybe you changed API keys recently)
    messages.warning(request, "Not authenticated")

  except stripe.error.APIConnectionError as e:
    # Network communication with Stripe failed
    messages.warning(request, "Network error")

  except stripe.error.StripeError as e:
    messages.warning(
        request, "Something went wrong. You were not charged. Please try again.")

  except Exception as e:
    messages.warning(request, "A serious error occurred.")

  return redirect('gameplay_error')
"""


def entry_page(request, entry_id):
  entry = get_single_entry(entry_id)
  context = {
      'entry': entry,
      'title': f'Entry - {entry.user.first_name} {entry.user.last_name}'
  }
  return render(request, 'gameplay/entry.html', context)


def user_entries_page(request):
  entries = Entry.objects.filter(user=request.user).order_by('-points')
  context = {
      'entries': entries,
      'title': 'My Entries'
  }
  return render(request, 'gameplay/entry_list.html', context)


def error_page(request):
  context = {
      'title': 'Error'
  }
  return render(request, 'gameplay/error_page.html', context)
