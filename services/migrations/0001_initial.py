# Generated by Django 4.2.2 on 2023-06-14 05:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='last-name')),
                ('email', models.EmailField(error_messages={'unique': 'An email is already registered'}, max_length=254, unique=True, verbose_name='email')),
                ('exprtise', models.CharField(choices=[('Debit', 'Debit'), ('Loans', 'Loans'), ('Demat', 'Demat'), ('Insurance', 'Insurance'), ('Account', 'Account')], max_length=10, verbose_name='expertise-in')),
                ('phone', models.BigIntegerField(verbose_name='phone')),
            ],
        ),
        migrations.CreateModel(
            name='QueryAssignedEmployee',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('assigned_query', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('task_status', models.BooleanField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='services.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeePerformanceReport',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('performance_report', models.DecimalField(decimal_places=2, max_digits=5)),
                ('query_assigned', models.ManyToManyField(to='services.queryassignedemployee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeExpertise',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('domain_experiance', models.IntegerField()),
                ('expertise', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='services.employee')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerQuery',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('query_type', models.CharField(choices=[('Debit', 'Debit'), ('Loans', 'Loans'), ('Demat', 'Demat'), ('Insurance', 'Insurance'), ('Account', 'Account')], max_length=10, verbose_name='query-type')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='customer-email')),
                ('raised_on', models.DateField(verbose_name='raised date')),
                ('resolved_on', models.DateField(blank=True, null=True, verbose_name='resolved date')),
                ('query_status', models.BooleanField()),
                ('resolved_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='services.employee')),
            ],
        ),
    ]
