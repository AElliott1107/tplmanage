from django import forms
from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory

PROVIDERS = (
    ('Service Provider 1', 'Service Provider 1'),
    ('Service Provider 2', 'Service Provider 2'),
    ('Service Provider 3', 'Service Provider 3'),
    ('Service Provider 4', 'Service Provider 4')
)


class ManagementForm(ModelForm):
    class Meta:
        model = Management
        fields = '__all__'
        widgets = {
            'manage_id': forms.HiddenInput
        }


class ResultForm(ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        widgets = {
            'result_id': forms.HiddenInput
        }


class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'
        widgets = {
            'pull_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'sample_id': forms.TextInput(attrs={'readonly': 'readonly'})
        }


class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ['study_id', 'project', 'provider', 'study_start', 'study_status']
        widgets = {
            'study_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            #'provider': forms.ChoiceField(choices=PROVIDERS),
            'study_start': forms.DateInput(attrs={'class': 'datepicker'})
        }
        labels = {
            'study_id': 'Study ID',
            'study_start': 'Study Start Date',
            'study_status': 'Study Status',
            'project': 'Project',
            'provider': 'Service Provider'
        }
