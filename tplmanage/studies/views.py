from django.shortcuts import render

from django.http import HttpResponse

from .models import Study

def index(request):
    studies = Study.objects.all()[:5]
    output = '<br>'.join([s.study_id for s in studies])
    return HttpResponse(output)
