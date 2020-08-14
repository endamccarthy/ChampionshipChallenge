from django import forms
from django.forms import DateTimeField

from gameplay.models import Fixture


class FixtureForm(forms.ModelForm):
  # first_name = forms.CharField(max_length=30, label='First Name')
  # last_name = forms.CharField(max_length=30, label='Last Name')

  class Meta:
    model = Fixture
    fields = ['team_A', 'team_B', 'datetime',
              'sport', 'region', 'fixture_round', 'location']
    widgets = {
        'datetime': forms.DateTimeInput(format=('%Y-%m-%d %H:%M'), attrs={'class': 'form-control', 'placeholder': 'Select a date and time', 'type': 'datetime-local'}),
    }
