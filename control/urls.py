from django.urls import path

from . import views as control_views

urlpatterns = [
    path('', control_views.control_home, name='control_home'),
    path('add-fixture/', control_views.control_add_fixture,
         name='control_add_fixture'),
    path('edit-fixture/<str:fixture_id>/', control_views.control_edit_fixture,
         name='control_edit_fixture'),
]
