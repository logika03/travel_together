# Generated by Django 3.1.7 on 2021-04-13 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210405_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='transport',
        ),
        migrations.AddField(
            model_name='trip',
            name='transport',
            field=models.ManyToManyField(to='main.Transport', verbose_name='Транспорт'),
        ),
    ]
