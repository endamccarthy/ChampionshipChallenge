"""championshipchallenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic import RedirectView

from users import views as user_views

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gameplay.urls')),
    path('details/', user_views.user_details, name='user_details'),
    path('deactivate/', user_views.deactivate_account, name='deactivate_account'),

    # override all these views to be redirected elsewhere
    path('accounts/email/',
         RedirectView.as_view(url=reverse_lazy('gameplay_error_page'), permanent=False)),
    path('accounts/confirm-email/',
         RedirectView.as_view(url=reverse_lazy('gameplay_error_page'), permanent=False)),
    re_path(r"^accounts/confirm-email/(?P<key>[-:\w]+)/$", RedirectView.as_view(
        url=reverse_lazy('gameplay_error_page'), permanent=False)),
    path('accounts/password/reset/key/done/',
         RedirectView.as_view(url=reverse_lazy('account_login'), permanent=False)),
    path('accounts/password/change/',
         RedirectView.as_view(url=reverse_lazy('account_reset_password'), permanent=False)),
    path('accounts/inactive/',
         RedirectView.as_view(url=reverse_lazy('gameplay_error_page'), permanent=False)),

    path('accounts/', include('allauth.urls')),
]

if settings.DEVELOPMENT_MODE:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)
