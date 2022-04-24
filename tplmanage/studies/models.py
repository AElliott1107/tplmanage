# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Study(models.Model):
    study_id = models.CharField(primary_key=True, max_length=50)
    project = models.CharField(max_length=50)
    provider = models.CharField(max_length=100)
    study_start = models.DateField(blank=True, null=True)
    study_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'study'

    def __str__(self):
        return self.study_id


class Sample(models.Model):
    sample_id = models.CharField(primary_key=True, max_length=50)
    study = models.ForeignKey('Study', on_delete=models.CASCADE)
    timepoint = models.FloatField(blank=True, null=True)
    pull_condition = models.CharField(max_length=50)
    quality = models.CharField(max_length=50, blank=True, null=True)
    pull_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sample'

    def __str__(self):
        return self.sample_id


class Management(models.Model):
    manage_id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    po_num = models.BigIntegerField()
    contract = models.CharField(max_length=100)
    shipment = models.CharField(max_length=50, blank=True, null=True)
    result_rec = models.DateField(blank=True, null=True)
    result_corr = models.CharField(max_length=50, blank=True, null=True)
    invoice_rec = models.DateField(blank=True, null=True)
    invoice_corr = models.CharField(max_length=50, blank=True, null=True)
    invoice_amt = models.FloatField(blank=True, null=True)
    po_current = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'management'

    def __str__(self):
        return self.manage_id


class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    reported = models.CharField(max_length=200, blank=True, null=True)
    component = models.CharField(max_length=100)
    test_name = models.CharField(max_length=100)
    result_status = models.CharField(max_length=50, blank=True, null=True)
    result_num = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'result'

    def __str__(self):
        return self.result_id
