from django.shortcuts import render
from django import forms
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse
from .models import Study, Sample, Management, Result
from .forms import StudyForm, SampleForm, ManagementForm, ResultForm
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


# CRUD View - Create a new study
class CreateStudy(CreateView):
    model = Study
    template_name = "studies/create.html"
    form_class = StudyForm

    # Update initial to create unique study ID
    def get_initial(self):
        today = datetime.datetime.today()
        initial = self.initial.copy()
        initial['study_id'] = 'APP' + str(today)
        return initial

    # Update context data to create dynamic parent/child entry for studies and samples
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_formset = forms.models.inlineformset_factory(Study, Sample, extra=1, form=SampleForm)
        if self.request.POST:
            context['formset'] = sample_formset(self.request.POST)
        else:
            context['formset'] = sample_formset()

    # Update form_valid to save the sample formset with the form
    def form_valid(self, form):
        response = super().form_valid(form)
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            print(form.errors)
            print(formset.errors)
            self.object.delete()
            return self.form_invalid(form, formset=formset)
        form.save()
        return response

    # Update form_invalid to include formset
    def form_invalid(self, form, **kwargs):
        formset = kwargs.pop('formset', None)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        url = reverse('studies:study-detail', kwargs={'pk': self.object.study_id})
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

    # Update form valid to save formset with form
    def form_valid(self, form):
        response = super().form_valid(form)
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            print(form.errors)
            print(formset.errors)
            return self.form_invalid(form, formset=formset)
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
    form_class = SampleForm
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
        url = reverse('studies:study-detail', kwargs={'pk': self.object.id})
        return url


# Service Provider Metrics View
def metrics(request):
    return render(request, 'studies/metrics.html')


# Study Result Data View
def trend_data(request):
    return render(request, 'studies/trend_data.html')