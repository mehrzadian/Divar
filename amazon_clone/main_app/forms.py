# main_app/forms.py

# main_app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password1', 'password2']

class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Phone number or username')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address']
