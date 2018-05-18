# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-18 21:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_kulukorvaus', '0006_auto_20180518_2131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kulukorvausperustiedot',
            options={'verbose_name': 'kulukorvaus perustiedot', 'verbose_name_plural': 'Kulukorvaus perustiedot'},
        ),
        migrations.AddField(
            model_name='kulukorvaus',
            name='info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_kulukorvaus.KulukorvausPerustiedot'),
        ),
    ]
