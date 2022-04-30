from django.shortcuts import render
from django import forms
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse
from .models import Study, Sample, Management, Result
from .forms import StudyForm, SampleForm, ManagementForm, ResultForm, SampleEditForm
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import pandas as pd
import numpy as np
import datetime


# Site Homepage
def index(request):
    return render(request, 'studies/index.html')


# Homepage for Studies
class StudiesHome(ListView):
    model = Study
    template_name = "studies/home.html"


# CRUD View - Read the details of a submitted study
class StudyDetail(DetailView):
    model = Study
    template_name = 'studies/detail.html'
    # Update context data to include samples attached to specific study
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pulls'] = self.object.sample_set.all()
        return context


# CRUD View - Read the details of a submitted sample
class SampleDetail(DetailView):
    model = Sample
    template_name = 'studies/sample_detail.html'
    # Update context data to include management and result info attached to specific sample
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = self.object.management_set.all()
        context['results'] = self.object.result_set.all()
        return context


# CRUD View - Create a new study
class CreateStudy(CreateView):
    model = Study
    template_name = "studies/create.html"
    form_class = StudyForm

    # Update initial to create unique study ID
    def get_initial(self):
        today = datetime.date.today()
        initial = self.initial.copy()
        try:
            id_list = list(Study.objects.filter(study_num__contains=str(today.year) + str(today.month) + str(today.day))
                           .order_by('study_num').values_list('study_num', flat=True))
            id_n = int(id_list[-1][-3:]) + 1

            # If no Form IDs exist for the year, start at Form Index 1
        except IndexError:
            id_n = int(1)
        initial['study_num'] = 'APP' + str(today.year) + str(today.month) + str(today.day) + '_' + str(id_n)
        return initial

    # Update context data to create dynamic parent/child entry for studies and samples
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_formset = forms.models.inlineformset_factory(Study, Sample, extra=1, form=SampleForm)
        if self.request.POST:
            context['formset'] = sample_formset(self.request.POST)
        else:
            context['formset'] = sample_formset()
        return context

    # Update form_valid to save the sample formset with the form
    def form_valid(self, form):
        response = super().form_valid(form)
        context = self.get_context_data()
        study_num = form.instance.study_num
        formset = context['formset']
        # Assign Sample ID and save formset
        count = 1
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            print(form.errors)
            print(formset.errors)
            self.object.delete()
            return self.form_invalid(form, formset=formset)

        for sample in formset:
            sample.instance.sample_num = str(study_num) + 'SA' + str(count)
            sample.save()
            count += 1
        form.save()
        return response

    # Update form_invalid to include formset
    def form_invalid(self, form, **kwargs):
        formset = kwargs.pop('samples', None)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        url = reverse('studies:study-detail', kwargs={'pk': self.object.id})
        return url


# CRUD View - Update an existing study, including add or deleting samples as needed
class StudyUpdate(UpdateView):
    model = Study
    form_class = StudyForm
    template_name = "studies/study_update.html"

    # Update context data for inline formset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_formset = forms.models.inlineformset_factory(Study, Sample, extra=1, can_delete=True, form=SampleForm)
        if self.request.POST:
            context['formset'] = sample_formset(self.request.POST, instance=self.object)
        else:
            context['formset'] = sample_formset(instance=self.object)
        return context

    # Update form valid to save formset with form
    def form_valid(self, form):
        response = super().form_valid(form)
        context = self.get_context_data()
        study_num = form.instance.study_num
        formset = context['formset']
        count = len(formset)
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            print(form.errors)
            print(formset.errors)
            return self.form_invalid(form, formset=formset)

        for sample in formset:
            if sample.instance.sample_num is None:
                sample.instance.sample_num = str(study_num) + 'SA' + str(count)
                sample.save()
            else:
                sample.save()
            count += 1
        form.save()
        return response

    # Update form invalid to include formset
    def form_invalid(self, form, **kwargs):
        formset = kwargs.pop('formset', None)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        url = reverse('studies:study-detail', kwargs={'pk': self.object.id})
        return url


# CRUD View - Update an existing sample to add management or result info
class SampleUpdate(UpdateView):
    model = Sample
    form_class = SampleEditForm
    template_name = "studies/sample_update.html"

    # Update context data for inline formset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        management_formset = forms.models.inlineformset_factory(Sample, Management, extra=1, can_delete=True,
                                                                form=ManagementForm)
        result_formset = forms.models.inlineformset_factory(Sample, Result, extra=1, can_delete=True, form=ResultForm)
        if self.request.POST:
            context['man_formset'] = management_formset(self.request.POST, instance=self.object)
            context['result_formset'] = result_formset(self.request.POST, instance=self.object)
        else:
            context['man_formset'] = management_formset(instance=self.object)
            context['result_formset'] = result_formset(instance=self.object)
        return context

    # Update form valid to save formset with form
    def form_valid(self, form):
        response = super().form_valid(form)
        context = self.get_context_data()
        man_formset = context['man_formset']
        result_formset = context['result_formset']
        if man_formset.is_valid():
            man_formset.instance = self.object
            man_formset.save()
        else:
            print(form.errors)
            print(man_formset.errors)
            return self.form_invalid(form, formset=man_formset)
        if result_formset.is_valid():
            result_formset.instance = self.object
            result_formset.save()
        else:
            print(form.errors)
            print(result_formset.errors)
            return self.form_invalid(form, formset=result_formset)
        form.save()
        return response

    # Update form invalid to include formset
    def form_invalid(self, form, **kwargs):
        formset = kwargs.pop('formset', None)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        url = reverse('studies:sample-detail', kwargs={'pk': self.object.id})
        return url


class MetricsCharts(TemplateView):
    template_name = "studies/metrics2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Queries
        mans = Management.objects.all().values('invoice_rec', 'invoice_corr', 'result_rec', 'result_corr',
                                               'invoice_amt', 'sample')
        samps = Sample.objects.all().values('id', 'sample_num', 'study', 'pull_date', 'study')
        studies = Study.objects.all().values('id', 'study_num', 'provider')
        # Data Frames
        data = pd.DataFrame(mans)
        data2 = pd.DataFrame(samps)
        data3 = pd.DataFrame(studies)
        merge1 = data3.merge(data2, how='left', left_on='id', right_on='study')
        full = merge1.merge(data, how='left', left_on='id_y', right_on='sample')

        # Add Invoice Corrections context for chart
        dfu = full.groupby(['provider', 'invoice_corr'])['id_x'].count().reset_index(name="count")
        context['in_label'] = dfu['provider'].drop_duplicates()
        context['in_no'] = list(dfu.loc[dfu['invoice_corr'] == 'No', 'count'])
        context['in_yes'] = list(dfu.loc[dfu['invoice_corr'] == 'Yes', 'count'])

        # Add Result Corrections context for chart
        r_df = full.groupby(['provider', 'result_corr'])['id_x'].count().reset_index(name="count")
        context['r_label'] = r_df['provider'].drop_duplicates()
        context['r_no'] = list(r_df.loc[r_df['result_corr'] == 'No', 'count'])
        context['r_yes'] = list(r_df.loc[r_df['result_corr'] == 'Yes', 'count'])

        # Add sample count by service provider context for chart
        c_df = full.groupby(['provider'])['sample'].count().reset_index(name="count")
        context['p_label'] = c_df['provider']
        context['p_count'] = c_df['count']
        return context


# Study Result Data View
class ResultCharts(TemplateView):
    template_name = "studies/trend_data.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Queries
        results = Result.objects.all().values('sample', 'test_name', 'component', 'result_num', 'reported')
        samps = Sample.objects.all().values('id', 'sample_num', 'study', 'pull_date', 'pull_condition', 'timepoint')
        studies = Study.objects.all().values('id', 'study_num', 'provider')

        # Data Frames
        data = pd.DataFrame(results)
        data2 = pd.DataFrame(samps)
        data3 = pd.DataFrame(studies)
        merge1 = data3.merge(data2, how='left', left_on='id', right_on='study')
        full = merge1.merge(data, how='left', left_on='id_y', right_on='sample')

        # Add Trend Example for Purity Data
        df1 = full[(full['study_num'] == 'STB00305008') & (full['component'] == 'Purity')]
        context['xs'] = df1['timepoint']
        context['ys'] = df1['result_num']

        # Add Sample Comparison across tests
        df2 = full[(full['study_num'] == 'STB00305008') & (full['component'] == 'Purity') &
                   ((full['sample_num'] == '9048')|(full['sample_num'] == '9050'))]
        tests = list(df2["test_name"].drop_duplicates())
        s48 = list(df2.loc[df2['sample_num'] == '9048', 'result_num'])
        s50 = list(df2.loc[df2['sample_num'] == '9050', 'result_num'])
        context['tests'] = tests
        context['s48'] = s48
        context['s50'] = s50

        return context
