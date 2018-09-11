# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-11 22:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prueba', models.CharField(max_length=200)),
                ('referencias', models.CharField(max_length=200)),
                ('resultados', models.CharField(max_length=200)),
                ('ultima_vez_modificado', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='LabExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('email_contacto', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True)),
                ('ultima_vez_modificado', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('registrado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laboratorios', to='accounts.ReceptionProfile')),
            ],
            options={
                'db_table': 'laboratorios',
            },
        ),
        migrations.CreateModel(
            name='LaboratoryProfile',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='laboratory_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_admin', models.BooleanField(default=False)),
                ('laboratorio_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_lab', to='labapp.Laboratorio')),
            ],
            options={
                'db_table': 'personal_labs',
            },
        ),
        migrations.AddField(
            model_name='labexam',
            name='laboratorio_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='procesos', to='labapp.Laboratorio'),
        ),
        migrations.AddField(
            model_name='labexam',
            name='manejado_por',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='examenes', to='labapp.LaboratoryProfile'),
        ),
        migrations.AddField(
            model_name='labexam',
            name='registrado_por',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examenes_de_labs', to='accounts.ReceptionProfile'),
        ),
        migrations.AddField(
            model_name='examresults',
            name='examen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultados', to='labapp.LabExam'),
        ),
    ]
