# Generated by Django 5.2.2 on 2025-06-25 04:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='penalty',
            name='issued_on',
        ),
        migrations.AddField(
            model_name='penalty',
            name='date_issued',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
