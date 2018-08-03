# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-03 06:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docapp', '0005_auto_20180802_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ant_familiares',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otalgia', models.BooleanField(default=False)),
                ('otaliquia_otorrea', models.BooleanField(default=False)),
                ('infeccion_oidos', models.BooleanField(default=False)),
                ('cuerpo_extranio_oido', models.BooleanField(default=False)),
                ('hipoacusia', models.BooleanField(default=False)),
                ('tumores_snc', models.BooleanField(default=False)),
                ('sarampion', models.BooleanField(default=False)),
                ('paperas', models.BooleanField(default=False)),
                ('sifilis', models.BooleanField(default=False)),
                ('rubeola', models.BooleanField(default=False)),
                ('cirugia_oido', models.BooleanField(default=False)),
                ('tinnitus', models.BooleanField(default=False)),
                ('mareo', models.BooleanField(default=False)),
                ('vertigo', models.BooleanField(default=False)),
                ('enfermedad_meniere', models.BooleanField(default=False)),
                ('hipertension', models.BooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False)),
                ('otro_familiar', models.TextField(blank=True, null=True)),
                ('audiology', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ant_familiares', to='docapp.Audiology')),
            ],
        ),
        migrations.CreateModel(
            name='Ant_otros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antineoplasicos', models.BooleanField(default=False)),
                ('metales_pesados', models.BooleanField(default=False)),
                ('vibraciones', models.BooleanField(default=False)),
                ('aminoglucosidos', models.BooleanField(default=False)),
                ('trauma_acustico', models.BooleanField(default=False)),
                ('servicio_militar_arma', models.BooleanField(default=False)),
                ('diureticos_asa', models.BooleanField(default=False)),
                ('exposicion_mercurio', models.BooleanField(default=False)),
                ('otro', models.TextField(blank=True, null=True)),
                ('audiology', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ant_otros', to='docapp.Audiology')),
            ],
        ),
        migrations.RemoveField(
            model_name='antecedentespf',
            name='audio_id',
        ),
        migrations.RenameField(
            model_name='estadoactual',
            old_name='aruido_molestia_frecuencia',
            new_name='ruido_molestia_frecuencia',
        ),
        migrations.RemoveField(
            model_name='ananmesis',
            name='audio_id',
        ),
        migrations.RemoveField(
            model_name='estadoactual',
            name='audio_id',
        ),
        migrations.RemoveField(
            model_name='exposiciones',
            name='audio_id',
        ),
        migrations.AddField(
            model_name='ananmesis',
            name='audiology',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ananmesis', to='docapp.Audiology'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadoactual',
            name='audiology',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='estado_actual', to='docapp.Audiology'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exposiciones',
            name='audiology',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exposiciones', to='docapp.Audiology'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='AntecedentesPF',
        ),
    ]
