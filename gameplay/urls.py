from django.urls import path

from . import views as gameplay_views

urlpatterns = [
    path('', gameplay_views.home_page, name='gameplay_home'),
    path('leaderboard/', gameplay_views.leaderboard_page,
         name='gameplay_leaderboard'),
    path('matches/', gameplay_views.matches_page, name='gameplay_matches'),
    path('create-entry/', gameplay_views.create_entry_page,
         name='gameplay_create_entry'),
    # path('checkout-page/<str:entry_id>/',
    #      gameplay_views.checkout_page, name='gameplay_checkout_page'),
    # path('checkout/<str:entry_id>/',
    #      gameplay_views.checkout, name='gameplay_checkout'),
    path('entry/<str:entry_id>/',
         gameplay_views.entry_page, name='gameplay_entry'),
    path('entries/', gameplay_views.user_entries_page,
         name='gameplay_user_entries'),
    path('error/', gameplay_views.error_page, name='gameplay_error'),
]
