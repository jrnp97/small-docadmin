""" model to save audiology form """
from django.db import models
from django.utils import timezone

from .general import ExamType
from accounts.models import DoctorProfile

class Audiology(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modify = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    exam_type = models.OneToOneField(ExamType, on_delete=models.CASCADE)
    create_by = models.ForeignKey(DoctorProfile, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return "Audiology"

    def get_exam_type(self):
        return self.exam_type.name

    def get_person(self):
        return self.exam_type.person.name

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

    audio_id = models.OneToOneField(Audiology, null=False, blank=False, on_delete=models.CASCADE)


class AntecedentesPF(models.Model):
    # Familiares
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

    # Otros antecedentes
    antineoplasicos = models.BooleanField(default=False, null=False, blank=True)
    metales_pesados = models.BooleanField(default=False, null=False, blank=True)
    vibraciones = models.BooleanField(default=False, null=False, blank=True)
    aminoglucosidos = models.BooleanField(default=False, null=False, blank=True)
    trauma_acustico = models.BooleanField(default=False, null=False, blank=True)
    servicio_militar_arma = models.BooleanField(default=False, null=False, blank=True)
    diureticos_asa = models.BooleanField(default=False, null=False, blank=True)
    exposicion_mercurio = models.BooleanField(default=False, null=False, blank=True)
    otro = models.TextField(null=True, blank=True)

    audio_id = models.OneToOneField(Audiology, null=False, blank=False, on_delete=models.CASCADE)


class Exposiciones(models.Model):

    OPTIONS = (
        ('si', 'Si'),
        ('no', 'No'),
        ('a veces', 'A veces')
    )
    # Uso
    audifonos = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    motocicleta = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    vehiculo_automotriz = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    maquinaria_pesada = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)

    # Tiempo exposicion
    audifonos_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    motocicleta_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    vehiculo_automotriz_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    maquinaria_pesada_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)

    # Frecuencia
    audifonos_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    motocicleta_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    vehiculo_automotriz_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    maquinaria_pesada_frecuencia = models.PositiveIntegerField(null=True, blank=True)

    # Tiempo de uso
    audifonos_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    motocicleta_tiempo_uso= models.PositiveIntegerField(null=True, blank=True)
    vehiculo_automotriz_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    maquinaria_pesada_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)

    # EPA
    audifonos_epa = models.PositiveIntegerField(null=True, blank=True)
    motocicleta_epa = models.PositiveIntegerField(null=True, blank=True)
    vehiculo_automotriz_epa = models.PositiveIntegerField(null=True, blank=True)
    maquinaria_pesada_epa = models.PositiveIntegerField(null=True, blank=True)

    audio_id = models.OneToOneField(Audiology, null=False, blank=False, on_delete=models.CASCADE)


class EstadoActual(models.Model):
    OPTIONS = (
        ('si', 'Si'),
        ('no', 'No'),
        ('a veces', 'A veces')
    )
    # Uso
    ruido_molestia = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    volumen_tv = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    frases_repetidas = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    escucha = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    escucha_ruido = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)

    # Tiempo exposicion
    ruido_molestia_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    volumen_tv_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frases_repetidas_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    escucha_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    escucha_ruido_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)

    # Frecuencia
    aruido_molestia_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    volumen_tv_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    frases_repetidas_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    escucha_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    escucha_ruido_frecuencia = models.PositiveIntegerField(null=True, blank=True)

    # Tiempo de uso
    ruido_molestia_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    volumen_tv_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    frases_repetidas_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    escucha_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    escucha_ruido_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)

    # EPA
    ruido_molestia_epa = models.PositiveIntegerField(null=True, blank=True)
    volumen_tv_epa = models.PositiveIntegerField(null=True, blank=True)
    frases_repetidas_epa = models.PositiveIntegerField(null=True, blank=True)
    escucha_epa = models.PositiveIntegerField(null=True, blank=True)
    escucha_ruido_epa = models.PositiveIntegerField(null=True, blank=True)

    audio_id = models.OneToOneField(Audiology, null=False, blank=False, on_delete=models.CASCADE)

