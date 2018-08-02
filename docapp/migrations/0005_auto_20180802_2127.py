# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-02 21:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docapp', '0004_auto_20180802_0231'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ant_enfermedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hipertension', models.BooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False)),
                ('colesterol_alto', models.BooleanField(default=False)),
                ('glaucoma', models.BooleanField(default=False)),
                ('migrania', models.BooleanField(default=False)),
                ('catarata', models.BooleanField(default=False)),
                ('cx_ocular', models.BooleanField(default=False)),
                ('trauma', models.BooleanField(default=False)),
                ('cuerpo_extranio', models.BooleanField(default=False)),
                ('hipermetropia', models.BooleanField(default=False)),
                ('miopia', models.BooleanField(default=False)),
                ('astigmatismo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ant_exam_externo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hiperemia', models.BooleanField(default=False)),
                ('pterigion', models.BooleanField(default=False)),
                ('descamacion_parpados', models.BooleanField(default=False)),
                ('secrecion', models.BooleanField(default=False)),
                ('pigmentacion', models.BooleanField(default=False)),
                ('estrabismo', models.BooleanField(default=False)),
                ('otros_examenes', models.TextField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ant_uso_lentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cerca', models.BooleanField(default=False)),
                ('lejos', models.BooleanField(default=False)),
                ('bifocales', models.BooleanField(default=False)),
                ('progresivos', models.BooleanField(default=False)),
                ('contacto', models.BooleanField(default=False)),
                ('oscuros', models.BooleanField(default=False)),
                ('filtro', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='antecedentes',
            name='visio_id',
        ),
        migrations.RenameField(
            model_name='sintomas',
            old_name='visio_id',
            new_name='vision',
        ),
        migrations.RemoveField(
            model_name='agudeza',
            name='visio_id',
        ),
        migrations.RemoveField(
            model_name='cronomatica',
            name='visio_id',
        ),
        migrations.AddField(
            model_name='agudeza',
            name='visio',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='agudeza', to='docapp.Visiometry'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cronomatica',
            name='vision',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cronomatica', to='docapp.Visiometry'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='visiometry',
            name='exam_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='visiometry', to='docapp.ExamType'),
        ),
        migrations.DeleteModel(
            name='Antecedentes',
        ),
        migrations.AddField(
            model_name='ant_uso_lentes',
            name='vision',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='antecedent_uso_lentes', to='docapp.Visiometry'),
        ),
        migrations.AddField(
            model_name='ant_exam_externo',
            name='vision',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='antecedent_exam_externo', to='docapp.Visiometry'),
        ),
        migrations.AddField(
            model_name='ant_enfermedad',
            name='vision',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='antecedent_sicks', to='docapp.Visiometry'),
        ),
    ]
