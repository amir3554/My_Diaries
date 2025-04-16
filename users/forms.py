from typing import Any
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import CustomUser

attrs = {'class' : 'form-control'}


class UserLoginForm(AuthenticationForm):
    
    def __init__(self,*args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs=attrs)
    )

    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs=attrs)
    )

class CustomUserCreationForm(UserCreationForm):
    
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs=attrs)
    )

    email = forms.CharField(
        label='email',
        widget=forms.TextInput(attrs=attrs)
    )

    first_name = forms.CharField(
        label='first_name',
        widget=forms.TextInput(attrs=attrs)
    )
    last_name = forms.CharField(
        label='last_name',
        widget=forms.TextInput(attrs=attrs)
    )
    
    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs=attrs)
    )

    password2 = forms.CharField(
        label='password confirmation',
        widget=forms.PasswordInput(attrs=attrs)
    )
    
    bio = forms.CharField(
        label='bio (Optional)',
        required=False,
        widget=forms.Textarea(attrs=attrs)
    )

    profile_image = forms.ImageField(
        label='profile_image',
        required=False,
        widget=forms.ClearableFileInput(attrs=attrs)
    )


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name',
                 'last_name', 'password1', 'password2', 'bio', 'profile_image']