# Generated by Django 3.1.7 on 2021-04-05 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210405_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_anonymous',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
