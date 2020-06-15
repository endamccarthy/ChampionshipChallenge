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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import include, path, reverse_lazy, re_path
from users import views as user_views
from . import settings
from django.shortcuts import redirect
from django.views.generic import RedirectView


urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('gameplay.urls')),
  path('account/', user_views.account, name='account'),
  path('accounts/email/', RedirectView.as_view(url=reverse_lazy('gameplay-error-page'), permanent=False)),
  path('accounts/confirm-email/', RedirectView.as_view(url=reverse_lazy('gameplay-error-page'), permanent=False)),
  re_path(r"^accounts/confirm-email/(?P<key>[-:\w]+)/$", RedirectView.as_view(url=reverse_lazy('gameplay-error-page'), permanent=False)),
  path('accounts/password/reset/key/done/', RedirectView.as_view(url=reverse_lazy('account_login'), permanent=False)),
  path('accounts/password/change/', RedirectView.as_view(url=reverse_lazy('account_reset_password'), permanent=False)),
  path('accounts/inactive/', RedirectView.as_view(url=reverse_lazy('gameplay-error-page'), permanent=False)),
  path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
