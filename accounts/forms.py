# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'The username or password is incorrect. Please try again.',
    }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('The username has already been registered。')

        if password1 != password2:
            raise forms.ValidationError('The passwords entered twice do not match.')

        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('The email has already been registered.')

        return cleaned_data
