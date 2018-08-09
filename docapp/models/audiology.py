""" model to save audiology form """
from django.db import models
from django.utils import timezone

from .general import ExamType
from accounts.models import DoctorProfile


class Audiology(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modify = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    exam_type = models.OneToOneField(ExamType, on_delete=models.CASCADE)
    create_by = models.ForeignKey(DoctorProfile,
                                  null=False,
                                  blank=False,
                                  on_delete=models.CASCADE,
                                  related_name='audiology_forms')

    def __str__(self):
        return self.last_modify

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        response = super(Audiology, self).save(force_insert, force_update, using, update_fields)
        self.exam_type.update_state()
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

    audiology = models.OneToOneField(Audiology, null=False, blank=False,
                                     on_delete=models.CASCADE, related_name='ananmesis')


class Ant_familiares(models.Model):
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

    audiology = models.OneToOneField(Audiology, null=False, blank=False,
                                     on_delete=models.CASCADE, related_name='ant_familiares')


class Ant_otros(models.Model):
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

    audiology = models.OneToOneField(Audiology, null=False, blank=False,
                                     on_delete=models.CASCADE, related_name='ant_otros')


class Exposiciones(models.Model):

    OPTIONS = (
        ('si', 'Si'),
        ('no', 'No'),
        ('a veces', 'A veces')
    )
    # Uso
    audifonos = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    audifonos_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    audifonos_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    audifonos_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    audifonos_epa = models.PositiveIntegerField(null=True, blank=True)

    motocicleta = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    motocicleta_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    motocicleta_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    motocicleta_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    motocicleta_epa = models.PositiveIntegerField(null=True, blank=True)

    vehiculo_automotriz = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    vehiculo_automotriz_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    vehiculo_automotriz_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    vehiculo_automotriz_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    vehiculo_automotriz_epa = models.PositiveIntegerField(null=True, blank=True)

    maquinaria_pesada = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    maquinaria_pesada_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    maquinaria_pesada_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    maquinaria_pesada_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    maquinaria_pesada_epa = models.PositiveIntegerField(null=True, blank=True)

    audiology = models.OneToOneField(Audiology, null=False, blank=False,
                                     on_delete=models.CASCADE, related_name='exposiciones')


class EstadoActual(models.Model):
    OPTIONS = (
        ('si', 'Si'),
        ('no', 'No'),
        ('a veces', 'A veces')
    )
    # Uso
    ruido_molestia = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    ruido_molestia_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    ruido_molestia_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    ruido_molestia_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    ruido_molestia_epa = models.PositiveIntegerField(null=True, blank=True)

    volumen_tv = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    volumen_tv_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    volumen_tv_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    volumen_tv_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    volumen_tv_epa = models.PositiveIntegerField(null=True, blank=True)

    frases_repetidas = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    frases_repetidas_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    frases_repetidas_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    frases_repetidas_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    frases_repetidas_epa = models.PositiveIntegerField(null=True, blank=True)

    escucha = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    escucha_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    escucha_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    escucha_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    escucha_epa = models.PositiveIntegerField(null=True, blank=True)

    escucha_ruido = models.CharField(max_length=10, choices=OPTIONS, null=False, blank=False)
    escucha_ruido_tiempo_exposicion = models.PositiveIntegerField(null=True, blank=True)
    escucha_ruido_frecuencia = models.PositiveIntegerField(null=True, blank=True)
    escucha_ruido_tiempo_uso = models.PositiveIntegerField(null=True, blank=True)
    escucha_ruido_epa = models.PositiveIntegerField(null=True, blank=True)
    # EPA
    audiology = models.OneToOneField(Audiology, null=False, blank=False,
                                     on_delete=models.CASCADE, related_name='estado_actual')

