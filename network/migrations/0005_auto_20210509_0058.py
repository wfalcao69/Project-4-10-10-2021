# Generated by Django 3.0.8 on 2021-05-09 03:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20210505_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_of_creation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
