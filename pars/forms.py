from django.forms import ModelForm
from django import forms

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={"class": 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={"class": 'form-input'}))


class DocumentUploadForm(forms.Form):
    document = forms.FileField(
        label='Выберите файл',
        widget=forms.FileInput(attrs={"class": 'f'})
    )
