from django import forms
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField
from .models import CustomUser


class CustomSignupForm(SignupForm):
  first_name = forms.CharField(max_length=30, label='First Name') 
  last_name = forms.CharField(max_length=30, label='Last Name')
  phone = PhoneNumberField(
    required=True, 
    label='Phone',
    help_text='Include country code (+353 for Ireland)',
    widget=forms.TextInput(attrs={'value': '+353 '})
  )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['email'].widget = forms.TextInput(attrs={'placeholder': ''})

  def signup(self, request, user): 
    user.first_name = self.cleaned_data['first_name'] 
    user.last_name = self.cleaned_data['last_name'] 
    user.phone = self.cleaned_data['phone']
    user.save() 
    return user


class UserUpdateForm(forms.ModelForm):
  first_name = forms.CharField(max_length=30, label='First Name') 
  last_name = forms.CharField(max_length=30, label='Last Name')
  phone = PhoneNumberField(
    required=True, 
    label='Phone',
    help_text='Include country code (+353 for Ireland)',
    widget=forms.TextInput(attrs={'value': '+353 '})
  )

  class Meta:
    model = CustomUser
    fields = ['email', 'first_name', 'last_name', 'phone']
