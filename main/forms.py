from .models import Raspisanie
from django.forms import ModelForm
from django import forms


class RaspisanieForm(ModelForm):
    class Meta:
        model = Raspisanie
        fields = ['weekday', 'date', 'teacher_name', 'subject', 'type_subject', 'auditory_name', 'time', 'group_name', 'subgroup']

class DocumentUploadForm(forms.Form):
    document = forms.FileField(label='Выберите файл')
