# Generated by Django 3.1.11 on 2021-06-08 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210607_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelparticipant',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips_participants', to=settings.AUTH_USER_MODEL, verbose_name='Участник'),
        ),
    ]
