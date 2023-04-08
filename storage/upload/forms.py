from django import forms
from .models import Files, RANKS, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .utils import bytes_to_mb


class ChangeRankForm(forms.ModelForm):
    rank = forms.ChoiceField(label='Оберіть рівень доступу', choices=RANKS, widget=forms.Select(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("rank",)


class FilesForm(forms.ModelForm):
    path = forms.FileField(label='Завантажте файл', widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Files
        fields = ('path',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FilesForm, self).__init__(*args, **kwargs)

    def clean_path(self):

        """ Валідація розміру та типу файлу залежно від тарифу користувача"""

        size = self.cleaned_data['path'].size
        name = str(self.cleaned_data['path'])
        file_extension = name.split('.')[-1].lower()

        if self.user.profile.rank == 'Junior' and size > 1048576:
            raise ValidationError(
                f'В вашому тарифі можливо загружати файли розміром менше 1 Мб. Змініть тариф'
                f' Розмір Вашого файлу {bytes_to_mb(size)} Mb')
        elif self.user.profile.rank == 'Middle' and size > 5242880:
            raise ValidationError(
                f'В вашому тарифі можливо загружати файли розміром менше 5 Мб. Змініть тариф'
                f' Розмір Вашого файлу {bytes_to_mb(size)} Mb')
        elif self.user.profile.rank == 'Senior' and size > 10485760:
            raise ValidationError(
                f'Максимальний розмір файлу 10 Мб.'
                f' Розмір Вашого файлу {bytes_to_mb(size)} Mb')
        elif self.user.profile.rank == 'Junior' and (file_extension not in ('jpeg', 'jpg')):
            raise ValidationError('В вашому тарифі можливо загружати лише .jpg файли')
        elif self.user.profile.rank != 'Junior' and file_extension not in ('jpg', 'jpeg', 'txt', 'pdf'):
            raise ValidationError('На даному ресурсі можливо загружати лише файли типу jpeg, txt і pdf ')
        return size


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Користувач',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введіть пароль',
                               widget=forms.PasswordInput(attrs={'class':'form-control'}))


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
