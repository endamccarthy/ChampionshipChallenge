from django.urls import path

from . import views as gameplay_views

urlpatterns = [
    path('', gameplay_views.get_home_page, name='gameplay_home'),
    path('leaderboard/', gameplay_views.get_leaderboard_page,
         name='gameplay_leaderboard'),
    path('fixtures/', gameplay_views.get_fixtures_page, name='gameplay_fixtures'),
    path('entry/', gameplay_views.get_create_entry_page,
         name='gameplay_create_entry'),
    path('checkout/<str:entry_id>/',
         gameplay_views.get_checkout_page, name='gameplay_checkout'),
    path('stripe_webhook/', gameplay_views.stripe_webhook, name='stripe_webhook'),
    path('entry/<str:entry_id>/',
         gameplay_views.get_entry_page, name='gameplay_entry'),
    path('entries/', gameplay_views.get_user_entries_page,
         name='gameplay_user_entries'),
    path('error/', gameplay_views.get_error_page, name='gameplay_error_page'),
]
