# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 09:58
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('notes', '0003_auto_20170509_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
