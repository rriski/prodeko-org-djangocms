# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-06 18:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_kulukorvaus', '0010_auto_20180830_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kulukorvauskulu',
            options={'verbose_name': 'kulukorvaus - yksittäiset kulut', 'verbose_name_plural': 'Kulukorvaukset - yksittäiset kulut'},
        ),
    ]
