""" model to save audiology form """
from django.db import models
from django.utils import timezone

from .general import TipoExamen
from accounts.models import DoctorProfile


class Audiology(models.Model):
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)

    tipo_examen = models.OneToOneField(TipoExamen, on_delete=models.CASCADE, related_name='audiologia')
    registrado_por = models.ForeignKey(DoctorProfile, null=False, blank=False, on_delete=models.PROTECT,
                                       related_name='formularios_audiologia')

    def __str__(self):
        return "Audiologia"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        response = super(Audiology, self).save(force_insert, force_update, using, update_fields)
        self.tipo_examen.update_state()
        return response

    class Meta:
        db_table = "exam_audiology"


class Ananmesis(models.Model):
    fecha_ultimo_examen = models.DateField(null=False, blank=False)
    causa = models.TextField(null=False, blank=False)
    INTER = (
        ('normal', 'Normal'),
        ('anormal', 'Anormal')
    )
    interpretacion = models.CharField(max_length=10, choices=INTER, null=False, blank=False)
    audiology = models.OneToOneField(Audiology, null=False, blank=False, primary_key=True,
                                     on_delete=models.CASCADE, related_name='ananmesis')


class AntFamiliares(models.Model):
    otalgia = models.BooleanField(default=False, null=False, blank=True)
    otaliquia_otorrea = models.BooleanField(default=False, null=False, blank=True)
    infeccion_oidos = models.BooleanField(default=False, null=False, blank=True)
    cuerpo_extranio_oido = models.BooleanField(default=False, null=False, blank=True)
    hipoacusia = models.BooleanField(default=False, null=False, blank=True)
    tumores_snc = models.BooleanField(default=False, null=False, blank=True)
    sarampion = models.BooleanField(default=False, null=False, blank=True)
    paperas = models.BooleanField(default=False, null=False, blank=True)
    sifilis = models.BooleanField(default=False, null=False, blank=True)
    rubeola = models.BooleanField(default=False, null=False, blank=True)
    cirugia_oido = models.BooleanField(default=False, null=False, blank=True)
    tinnitus = models.BooleanField(default=False, null=False, blank=True)
    mareo = models.BooleanField(default=False, null=False, blank=True)
    vertigo = models.BooleanField(default=False, null=False, blank=True)
    enfermedad_meniere = models.BooleanField(default=False, null=False, blank=True)
    hipertension = models.BooleanField(default=False, null=False, blank=True)
    diabetes = models.BooleanField(default=False, null=False, blank=True)
    otro_familiar = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    audiology = models.OneToOneField(Audiology, primary_key=True, on_delete=models.CASCADE,
                                     related_name='antecedentes_familiares')


class OtrosAntecedentes(models.Model):
    antineoplasicos = models.BooleanField(default=False, null=False, blank=True)
    metales_pesados = models.BooleanField(default=False, null=False, blank=True)
    vibraciones = models.BooleanField(default=False, null=False, blank=True)
    aminoglucosidos = models.BooleanField(default=False, null=False, blank=True)
    trauma_acustico = models.BooleanField(default=False, null=False, blank=True)
    servicio_militar_arma = models.BooleanField(default=False, null=False, blank=True)
    diureticos_asa = models.BooleanField(default=False, null=False, blank=True)
    exposicion_mercurio = models.BooleanField(default=False, null=False, blank=True)
    otros = models.TextField(null=True, blank=True)

    audiology = models.OneToOneField(Audiology, primary_key=True, on_delete=models.CASCADE,
                                     related_name='otros_antecedentes')


OPCIONES = (('si', 'Si'),
            ('no', 'No'),
            ('a veces', 'A veces'),)


# Exposiciones opciones
class Exposiciones(models.Model):
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiology = models.OneToOneField(Audiology, null=False, blank=False,
                                     on_delete=models.CASCADE, related_name='exposiciones')


class ExposicionAudifonos(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    exposicion = models.OneToOneField(Exposiciones, related_name='audifonos')


class ExposicionMotocicleta(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    exposicion = models.OneToOneField(Exposiciones, related_name='motocicleta')


class ExposicionAutomotriz(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    exposicion = models.OneToOneField(Exposiciones, related_name='automotriz')


class ExposicionMaquinariaPesada(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    exposicion = models.OneToOneField(Exposiciones, related_name='maquinaria_pesada')


# Estado Actual opciones
class EstadoActual(models.Model):
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiology = models.OneToOneField(Audiology, null=False, blank=False,
                                     on_delete=models.CASCADE, related_name='estado_actual')


class RuidoMolestia(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    estado_actual = models.OneToOneField(EstadoActual, related_name='ruido_molestia')


class VolumenTv(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    estado_actual = models.OneToOneField(EstadoActual, related_name='volumen_tv')


class FrasesRepetidas(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    estado_actual = models.OneToOneField(EstadoActual, related_name='frases_repetidas')


class Escucha(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    estado_actual = models.OneToOneField(EstadoActual, related_name='escucha')


class EscuchaRuido(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    estado_actual = models.OneToOneField(EstadoActual, related_name='escucha_ruido')


class Information(models.Model):
    interpretaciones = models.TextField(null=False, blank=False)
    recomendaciones = models.TextField(null=True, blank=True)
    audiology = models.OneToOneField(Audiology, primary_key=True, on_delete=models.CASCADE, related_name='informacion')


class Otoscopia(models.Model):
    otoscopia_izq = models.ImageField(upload_to='otoscopia/%Y/%m/%d/')
    otoscopia_der = models.ImageField(upload_to='otoscopia/%Y/%m/%d/')

    audiology = models.OneToOneField(Audiology, primary_key=True, on_delete=models.CASCADE, related_name='otoscopia')
