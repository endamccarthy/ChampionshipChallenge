from django.db import models
from django.utils import timezone
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# def get_sentinel_user():
#   return get_user_model().objects.get_or_create(username='deleted')[0]


class Entry(models.Model):
  # user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
  points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
  date_posted = models.DateTimeField(default=timezone.now)

  # def __str__(self):
  #   return self.user.get_username()