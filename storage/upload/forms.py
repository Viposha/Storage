from django import forms
from .models import Files, RANKS
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class FilesForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('path',)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Користувач', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введіть пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UserCreateForm(UserCreationForm):
    rank = forms.ChoiceField(label='Оберіть рівень доступу', choices=RANKS, widget=forms.Select(
        attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=150, label='Користувач', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Введіть пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password2 = forms.CharField(label='Підтвердіть пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "rank")

