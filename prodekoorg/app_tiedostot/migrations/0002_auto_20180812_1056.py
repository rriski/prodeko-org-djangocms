# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-12 10:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_tiedostot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TiedostoVersio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('modified_date', models.DateField(auto_now=True)),
                ('file', models.FileField(unique=True, upload_to='files')),
            ],
            options={
                'verbose_name_plural': 'Tiedostoversiot',
            },
        ),
        migrations.AlterModelOptions(
            name='tiedosto',
            options={'verbose_name_plural': 'Tiedostot'},
        ),
        migrations.RemoveField(
            model_name='tiedosto',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='tiedosto',
            name='file',
        ),
        migrations.RemoveField(
            model_name='tiedosto',
            name='modified_date',
        ),
        migrations.AddField(
            model_name='tiedosto',
            name='title',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='tiedosto',
            name='thumbnail_image',
            field=models.ImageField(blank=True, null=True, upload_to='file_thumbnail_images'),
        ),
        migrations.AddField(
            model_name='tiedostoversio',
            name='tiedosto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='app_tiedostot.Tiedosto'),
        ),
    ]