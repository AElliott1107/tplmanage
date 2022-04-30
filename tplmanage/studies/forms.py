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
        labels = {
            'po_num': '',
            'po_current': '',
            'invoice_amt': '',
            'invoice_rec': '',
            'invoice_corr': '',
            'result_rec': '',
            'result_corr': '',
            'shipment': '',
            'contract': ''
        }
        help_texts = {
            'invoice_rec': 'Please enter in YYYY-MM-DD format.',
            'result_rec': 'Please enter in YYYY-MM-DD format.'
        }


class ResultForm(ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        widgets = {
            'result_id': forms.HiddenInput
        }
        labels = {
            'result_num': '',
            'reported': '',
            'result_status': '',
            'test_name': '',
            'component': ''
        }


class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput,
            'pull_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'sample_num': forms.TextInput(attrs={'readonly': 'readonly'})
        }
        labels = {
            'sample_num': '',
            'pull_date': '',
            'pull_condition': '',
            'timepoint': '',
            'quality': ''
        }
        help_texts = {
            'sample_num': 'Automatically Assigned',
            'pull_date': 'Please enter in YYYY-MM-DD format.',
            'timepoint': 'Please enter number of months.'
        }


class SampleEditForm(ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput,
            'pull_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'sample_num': forms.TextInput(attrs={'readonly': 'readonly'}),
            'study': forms.HiddenInput
        }
        labels = {
            'sample_num': '',
            'pull_date': '',
            'pull_condition': '',
            'timepoint': '',
            'quality': ''
        }
        help_texts = {
            'sample_num': 'Automatically Assigned',
            'pull_date': 'Please enter in YYYY-MM-DD format.',
            'timepoint': 'Please enter number of months.'
        }


class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = '__all__'
        widgets = {
            'study_num': forms.TextInput(attrs={'readonly': 'readonly'}),
            'study_start': forms.DateInput(attrs={'class': 'datepicker'})
        }
        labels = {
            'study_num': 'Study ID',
            'study_start': 'Study Start Date',
            'study_status': 'Study Status',
            'project': 'Project',
            'provider': 'Service Provider'
        }
        help_texts = {
            'study_start': 'Please enter in YYYY-MM-DD format.'
        }
