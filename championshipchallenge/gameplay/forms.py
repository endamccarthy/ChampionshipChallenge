from crispy_forms.helper import FormHelper
from django import forms
# from django.http import request

from .models import Entry, Finalist, Prediction


class EntryForm(forms.ModelForm):
  class Meta:
    model = Entry
    fields = '__all__'


class PredictionForm(forms.ModelForm):
  class Meta:
    model = Prediction
    fields = ['fixture', 'prediction']

  def __init__(self, *args, **kwargs):
    super(PredictionForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_show_labels = False


class FinalistForm(forms.ModelForm):
  class Meta:
    model = Finalist
    fields = ['team_A', 'team_B']

  def __init__(self, *args, **kwargs):
    super(FinalistForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_show_labels = False
