from django.urls import path
from . import views as gameplay_views


urlpatterns = [
  path('', gameplay_views.home, name='gameplay_home'),
  path('leaderboard/', gameplay_views.leaderboard, name='gameplay_leaderboard'),
  path('fixtures/', gameplay_views.fixtures, name='gameplay_fixtures'),
  path('entry/', gameplay_views.create_entry, name='gameplay_create_entry'),
  path('checkout/<str:entry_id>/', gameplay_views.checkout, name='gameplay_checkout'),
  path('entry/<str:entry_id>/', gameplay_views.entry, name='gameplay_entry'),
  path('entries/', gameplay_views.user_entries, name='gameplay_user_entries'),
  path('error/', gameplay_views.error_page, name='gameplay_error_page'),
]