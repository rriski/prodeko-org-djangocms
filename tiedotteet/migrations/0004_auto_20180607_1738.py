# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-07 17:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiedotteet', '0003_auto_20180606_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='deadline_date',
            field=models.DateField(blank=True, default=datetime.date(2018, 6, 14), null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='end_date',
            field=models.DateField(default=datetime.date(2018, 6, 14)),
        ),
    ]