# Generated by Django 4.2.2 on 2023-07-02 04:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parking', '0003_parkingspot_hourly_charge'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestedParking',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('booked_on', models.DateTimeField(auto_now_add=True)),
                ('hours_for', models.IntegerField()),
                ('payable_amount', models.FloatField(blank=True, null=True)),
                ('booked_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_booked_by', to=settings.AUTH_USER_MODEL)),
                ('parking_spot', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_parking_spot', to='parking.parkingspot')),
            ],
        ),
        migrations.DeleteModel(
            name='ParkingRequested',
        ),
    ]
