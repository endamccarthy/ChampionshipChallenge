from django.urls import path
from . import views as gameplay_views


urlpatterns = [
  path('', gameplay_views.home, name='gameplay_home'),
  path('entry/', gameplay_views.entry, name='gameplay_entry'),
  path('error_page/', gameplay_views.error_page, name='gameplay_error_page'),
]