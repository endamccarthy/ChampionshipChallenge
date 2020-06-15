from django import forms
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField


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
    # self.fields['email'].label = 'test'
    self.fields['email'].widget = forms.TextInput(attrs={'placeholder': ''})
    # self.fields['password1'].widget = forms.PasswordInput
    # print(dir(self.fields['password1']))
    print(self.fields['password1'].help_text)
    # self.fields['email'] = forms.EmailField(label='Email')
    # self.fields['password'] = forms.PasswordField(label='Email')

  def signup(self, request, user): 
    user.first_name = self.cleaned_data['first_name'] 
    user.last_name = self.cleaned_data['last_name'] 
    user.phone = self.cleaned_data['phone']
    user.save() 
    return user