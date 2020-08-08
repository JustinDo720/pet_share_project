from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='Please type in your email. NOTE: This is not required')

    class Meta:
        model = User
        fields = ['username','email','password1','password2']