from django.urls import path
from . import views as gameplay_views


urlpatterns = [
  path('', gameplay_views.home, name='gameplay-home'),
  path('error_page/', gameplay_views.error_page, name='gameplay-error-page'),
]