from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from test_dog_app.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='Please type in your email. NOTE: This is not required')

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class ChangeProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_photo']
        labels = {'user_photo': 'Change Picture: '}


class ChangeUserNameForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email']
