from django import forms

from gameplay.models import Fixture


class FixtureForm(forms.ModelForm):
  # first_name = forms.CharField(max_length=30, label='First Name')
  # last_name = forms.CharField(max_length=30, label='Last Name')

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['datetime'].widget = forms.DateTimeInput(
        format='%Y-%m-%d %H:%M', attrs={'class': 'datetimefield'})

  class Meta:
    model = Fixture
    fields = ['team_A', 'team_B', 'datetime',
              'sport', 'region', 'fixture_round', 'location']
