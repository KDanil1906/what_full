from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'login__general-input', 'placeholder': 'Введите имя пользователя', 'type': 'text'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login__general-input', 'placeholder': 'Введите пароль', 'type': 'password'
    }))


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'registration__general-input', 'placeholder': 'Введите имя пользователя', 'type': 'text'
    }))

    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'registration__general-input', 'placeholder': 'Введите пароль', 'type': 'password'
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'registration__general-input', 'placeholder': 'Введите email', 'type': 'email'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']
