from django.urls import path
from . import views as gameplay_views


urlpatterns = [
  path('', gameplay_views.home, name='gameplay-home'),
]