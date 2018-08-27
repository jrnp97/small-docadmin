# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-27 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docapp', '0002_auto_20180826_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacienteempresa',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default.png', null=True, upload_to='avatars/patients_company'),
        ),
        migrations.AlterField(
            model_name='pacienteparticular',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default.png', null=True, upload_to='avatars/patients_particular'),
        ),
    ]