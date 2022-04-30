from django.contrib import admin
from .models import Study, Sample, Management, Result

class ResultInline(admin.TabularInline):
    model = Result
    extra = 1
    fieldsets = [
        (None, {'fields': ('test_name', 'component', 'result_status', 'result_num', 'reported')})
    ]


class ManagementInline(admin.TabularInline):
    model = Management
    extra = 1
    fieldsets = [
        (None, {'fields': ('po_num', 'contract', 'shipment', 'result_rec', 'result_corr', 'invoice_rec', 'invoice_corr',
                           'invoice_amt', 'po_current')})
    ]


class SampleInline(admin.TabularInline):
    model = Sample
    extra = 1
    fieldsets = [
        (None, {'fields': ('timepoint', 'pull_condition', 'quality', 'pull_date', 'sample_num')})
    ]


class SampleAdmin(admin.ModelAdmin):
    inlines = [ResultInline, ManagementInline]


class StudyAdmin(admin.ModelAdmin):
    inlines = [SampleInline]


# Register your models here.
admin.site.register(Study, StudyAdmin)
admin.site.register(Sample, SampleAdmin)

