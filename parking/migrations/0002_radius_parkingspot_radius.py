# Generated by Django 4.2.2 on 2023-07-02 04:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Radius',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('range', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='parkingspot',
            name='radius',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='parking.radius'),
        ),
    ]
