from typing import Any
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import CustomUser

attr = {'class' : 'form-control'}


class UserLoginForm(AuthenticationForm):
    
    def __init__(self,*args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs=attr)
    )

    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs=attr)
    )

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'bio', 'profile_image',]