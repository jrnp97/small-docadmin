""" model to save audiology form """
from django.db import models
from .general import ExamType, User


class Audiology(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modify = models.DateTimeField(null=True, blank=True)
    exam_type = models.OneToOneField(ExamType, on_delete=models.CASCADE)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Audiology"

    def get_exam_type(self):
        return self.exam_type.name

    def get_person(self):
        return self.exam_type.person.name


class Ananmesis(models.Model):
    fecha_ultimo_examen = models.DateField(null=False, blank=False)
    causa = models.TextField(null=False, blank=False)

    INTER = (
        ('normal', 'Normal'),
        ('anormal', 'Anormal')
    )
    interpretacion = models.CharField(max_length=10, choices=INTER, null=False, blank=False)

    audio_id = models.OneToOneField(Audiology, on_delete=models.CASCADE)


class AntecedentesPF(models.Model):
    otalgia = models.BooleanField(default=False)
    otaliquia_otorrea = models.BooleanField(default=False)
    infeccion_oidos = models.BooleanField(default=False)
    cuerpo_extranio_oido = models.BooleanField(default=False)
    hipoacusia = models.BooleanField(default=False)
    tumores_snc = models.BooleanField(default=False)
    sarampion = models.BooleanField(default=False)
    paperas = models.BooleanField(default=False)
    sifilis = models.BooleanField(default=False)
    rubeola = models.BooleanField(default=False)
    cirugia_oido = models.BooleanField(default=False)
    tinnitus = models.BooleanField(default=False)
    mareo = models.BooleanField(default=False)
    vertigo = models.BooleanField(default=False)
    enfermedad_meniere = models.BooleanField(default=False)
    hipertension = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)

    otro = models.TextField(null=True, blank=True)

    audio_id = models.OneToOneField(Audiology, on_delete=models.CASCADE)


class OtrosAntecedentes(models.Model):
    antineoplasicos = models.BooleanField(default=False)
    metales_pesados = models.BooleanField(default=False)
    vibraciones = models.BooleanField(default=False)
    aminoglucosidos = models.BooleanField(default=False)
    trauma_acustico = models.BooleanField(default=False)
    servicio_militar_arma = models.BooleanField(default=False)
    diureticos_asa = models.BooleanField(default=False)
    exposicion_mercurio = models.BooleanField(default=False)

    otro = models.TextField(null=True, blank=True)

    audio_id = models.OneToOneField(Audiology, on_delete=models.CASCADE)


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

    audio_id = models.OneToOneField(Audiology, on_delete=models.CASCADE)


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

    audio_id = models.OneToOneField(Audiology, on_delete=models.CASCADE)

