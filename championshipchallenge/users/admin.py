from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser

admin.site.login = login_required(admin.site.login)

# Custom admin view for the user account


@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
  """Define admin model for custom User model with no email field."""

  fieldsets = (
      (None, {'fields': ('email', 'password')}),
      (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
      (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                     'is_superuser', 'groups', 'user_permissions')}),
      (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
  )
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'phone', 'password1', 'password2'),
      }),
  )
  list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff')
  search_fields = ('email', 'first_name', 'last_name', 'phone')
  ordering = ('email',)
