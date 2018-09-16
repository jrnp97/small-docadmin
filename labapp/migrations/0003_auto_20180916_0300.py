# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-16 03:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labapp', '0002_auto_20180916_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labexam',
            name='manejado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='examenes', to='labapp.LaboratoryProfile'),
        ),
    ]
