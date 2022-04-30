# Generated by Django 4.0.4 on 2022-04-27 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Management',
            fields=[
                ('manage_id', models.AutoField(primary_key=True, serialize=False)),
                ('po_num', models.BigIntegerField()),
                ('contract', models.CharField(max_length=100)),
                ('shipment', models.CharField(blank=True, max_length=50, null=True)),
                ('result_rec', models.DateField(blank=True, null=True)),
                ('result_corr', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_rec', models.DateField(blank=True, null=True)),
                ('invoice_corr', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_amt', models.FloatField(blank=True, null=True)),
                ('po_current', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'management',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('result_id', models.AutoField(primary_key=True, serialize=False)),
                ('reported', models.CharField(blank=True, max_length=200, null=True)),
                ('component', models.CharField(max_length=100)),
                ('test_name', models.CharField(max_length=100)),
                ('result_status', models.CharField(blank=True, max_length=50, null=True)),
                ('result_num', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'result',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_num', models.CharField(blank=True, max_length=50, null=True)),
                ('timepoint', models.FloatField(blank=True, null=True)),
                ('pull_condition', models.CharField(max_length=50)),
                ('quality', models.CharField(blank=True, max_length=50, null=True)),
                ('pull_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sample',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_num', models.CharField(max_length=50)),
                ('project', models.CharField(max_length=50)),
                ('provider', models.CharField(max_length=100)),
                ('study_start', models.DateField(blank=True, null=True)),
                ('study_status', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'study',
                'managed': False,
            },
        ),
    ]
