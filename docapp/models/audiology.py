""" model to save audiology form """
from django.db import models
from django.utils import timezone

from .general import Examinacion


class Audiology(models.Model):
    examinacion_id = models.OneToOneField(Examinacion, on_delete=models.CASCADE, related_name='audiologia')
    estado_general = models.TextField(null=False, blank=False)

    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)

    def __str__(self):
        return "Audiologia"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        response = super(Audiology, self).save(force_insert, force_update, using, update_fields)
        self.examinacion_id.update_doctor()
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
    audiologia_id = models.OneToOneField(Audiology, null=False, blank=False, primary_key=True,
                                         on_delete=models.CASCADE, related_name='ananmesis')


class AntFamiliares(models.Model):
    """ Model to save if a pacient present some antecedent from family default (no present) """
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
    observaciones = models.TextField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, on_delete=models.CASCADE, related_name='antecedentes_familiares')


class OtrosAntecedentes(models.Model):
    """ Model to save if a pacient present some antecedent default (no present) """
    antineoplasicos = models.BooleanField(default=False, null=False, blank=True)
    metales_pesados = models.BooleanField(default=False, null=False, blank=True)
    vibraciones = models.BooleanField(default=False, null=False, blank=True)
    aminoglucosidos = models.BooleanField(default=False, null=False, blank=True)
    trauma_acustico = models.BooleanField(default=False, null=False, blank=True)
    servicio_militar_arma = models.BooleanField(default=False, null=False, blank=True)
    diureticos_asa = models.BooleanField(default=False, null=False, blank=True)
    exposicion_mercurio = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, on_delete=models.CASCADE, related_name='otros_antecedentes')


OPCIONES = (('si', 'Si'),
            ('no', 'No'),
            ('a veces', 'A veces'),)


# Exposiciones opciones
class ExposicionAudifonos(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, null=False, blank=False,
                                         on_delete=models.CASCADE, related_name='exposicion_audifonos')


class ExposicionMotocicleta(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, null=False, blank=False,
                                         on_delete=models.CASCADE, related_name='exposicion_motocicleta')


class ExposicionAutomotriz(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, null=False, blank=False,
                                         on_delete=models.CASCADE, related_name='exposicion_automotriz')


class ExposicionMaquinariaPesada(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, null=False, blank=False,
                                         on_delete=models.CASCADE, related_name='exposicion_maquinaria_pesada')


# Estado Actual opciones
class RuidoMolestia(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, null=False, blank=False,
                                         on_delete=models.CASCADE, related_name='estado_actual_ruido_molestia')


class VolumenTv(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, null=False, blank=False,
                                         on_delete=models.CASCADE, related_name='estado_actual_volumen_tv')


class FrasesRepetidas(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, null=False, blank=False,
                                         on_delete=models.CASCADE, related_name='estado_actual_frases_repetidas')


class Escucha(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, null=False, blank=False,
                                         on_delete=models.CASCADE, related_name='estado_actual_escucha')


class EscuchaRuido(models.Model):
    estado = models.CharField(max_length=10, choices=OPCIONES, null=False, blank=False)
    tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frecuencia = models.PositiveIntegerField(null=True, blank=True)
    tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    epa = models.PositiveIntegerField(null=True, blank=True)
    audiologia_id = models.OneToOneField(Audiology, null=False, blank=False,
                                         on_delete=models.CASCADE, related_name='estado_actual_escucha_ruido')


# Audiometria Section
class Audiometria(models.Model):
    ESTADO = (
        ('normal', 'Normal'),
        ('anormal', 'Anormal')
    )
    otoscopia_ojo_izquierdo = models.CharField(max_length=10, choices=ESTADO, default='normal', null=False, blank=False)
    otoscopia_ojo_derecho = models.CharField(max_length=10, choices=ESTADO, default='normal', null=False, blank=False)
    observaciones_otoscopia = models.TextField()

    resultados_oidos = models.ImageField(upload_to='otoscopia/%Y/%m/%d/', null=True, blank=True)

    interpretaciones_oido_derecho = models.TextField(null=False, blank=False)
    interpretaciones_oido_izquierdo = models.TextField(null=False, blank=False)
    recomendaciones = models.TextField(null=True, blank=True)

    audiologia_id = models.OneToOneField(Audiology, primary_key=True, on_delete=models.CASCADE,
                                         related_name='audiometria')
