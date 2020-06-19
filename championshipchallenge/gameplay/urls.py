from django.urls import path
from . import views as gameplay_views


urlpatterns = [
  path('', gameplay_views.home, name='gameplay_home'),
  path('error_page/', gameplay_views.error_page, name='gameplay_error_page'),
]