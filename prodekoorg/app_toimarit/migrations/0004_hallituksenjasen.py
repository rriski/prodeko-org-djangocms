# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-14 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_toimarit', '0003_auto_20180812_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='HallituksenJasen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etunimi', models.CharField(max_length=30)),
                ('sukunimi', models.CharField(max_length=30)),
                ('virka', models.CharField(max_length=50)),
                ('jaosto', models.CharField(max_length=100)),
                ('virka_eng', models.CharField(blank=True, max_length=60)),
                ('puhelin', models.CharField(blank=True, max_length=20)),
                ('sahkoposti', models.CharField(blank=True, max_length=30)),
            ],
            options={
                'verbose_name_plural': 'hallituksen jäsenet',
            },
        ),
    ]
