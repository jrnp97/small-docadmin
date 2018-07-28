"""model to save visiometry form"""
from django.utils import timezone
from django.db import models

from .general import ExamType
from accounts.models import DoctorProfile


class Visiometry(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modify = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    exam_type = models.OneToOneField(ExamType, null=False, blank=False, on_delete=models.CASCADE)
    create_by = models.ForeignKey(DoctorProfile,
                                  null=False,
                                  blank=False,
                                  on_delete=models.CASCADE,
                                  related_name='visiometry_forms')

    def __str__(self):
        return self.exam_type.name

    class Meta:
        db_table = "exam_visiometria"


class Sintomas(models.Model):
    ardor = models.BooleanField(default=False, null=False, blank=True)
    dolor = models.BooleanField(default=False, null=False, blank=True)
    cefalea = models.BooleanField(default=False, null=False, blank=True)
    fatiga_visual = models.BooleanField(default=False, null=False, blank=True)
    lagrimeo = models.BooleanField(default=False, null=False, blank=True)
    fotofobia = models.BooleanField(default=False, null=False, blank=True)
    cansansio_lectura = models.BooleanField(default=False, null=False, blank=True)
    prurito = models.BooleanField(default=False, null=False, blank=True)
    lectura_salto_lineas = models.BooleanField(default=False, null=False, blank=True)
    secreciones = models.BooleanField(default=False, null=False, blank=True)
    mala_vision_lejos = models.BooleanField(default=False, null=False, blank=True)
    mala_vision_cerca = models.BooleanField(default=False, null=False, blank=True)

    observaciones = models.TextField(null=True, blank=True)

    visio_id = models.OneToOneField(Visiometry, null=False, blank=False, on_delete=models.CASCADE)

    # ardor_description = models.TextField(null=True, blank=True)
    # dolor_description = models.TextField(null=True, blank=True)
    # cefalea_description = models.TextField(null=True, blank=True)
    # fatiga_visual_description = models.TextField(null=True, blank=True)
    # lagrimeo_description = models.TextField(null=True, blank=True)
    # fotofobia_description = models.TextField(null=True, blank=True)
    # cansansio_lectura_description = models.TextField(null=True, blank=True)
    # prurito_description = models.TextField(null=True, blank=True)
    # lectura_salto_lineas_description = models.TextField(null=True, blank=True)
    # secreciones_description = models.TextField(null=True, blank=True)
    # mala_vision_lejos_description = models.TextField(null=True, blank=True)
    # mala_vision_cerca_description = models.TextField(null=True, blank=True)


class Antecedentes(models.Model):
    # Enfermedad
    hipertension = models.BooleanField(default=False, null=False, blank=True)
    diabetes = models.BooleanField(default=False, null=False, blank=True)
    colesterol_alto = models.BooleanField(default=False, null=False, blank=True)
    glaucoma = models.BooleanField(default=False, null=False, blank=True)
    migrania = models.BooleanField(default=False, null=False, blank=True)
    catarata = models.BooleanField(default=False, null=False, blank=True)
    cx_ocular = models.BooleanField(default=False, null=False, blank=True)
    trauma = models.BooleanField(default=False, null=False, blank=True)
    cuerpo_extranio = models.BooleanField(default=False, null=False, blank=True)
    hipermetropia = models.BooleanField(default=False, null=False, blank=True)
    miopia = models.BooleanField(default=False, null=False, blank=True)
    astigmatismo = models.BooleanField(default=False, null=False, blank=True)

    # Uso de lentes
    cerca = models.BooleanField(default=False, null=False, blank=True)
    lejos = models.BooleanField(default=False, null=False, blank=True)
    bifocales = models.BooleanField(default=False, null=False, blank=True)
    progresivos = models.BooleanField(default=False, null=False, blank=True)
    contacto = models.BooleanField(default=False, null=False, blank=True)
    oscuros = models.BooleanField(default=False, null=False, blank=True)
    filtro = models.BooleanField(default=False, null=False, blank=True)

    # Examen Externo
    hiperemia = models.BooleanField(default=False, null=False, blank=True)
    pterigion = models.BooleanField(default=False, null=False, blank=True)
    descamacion_parpados = models.BooleanField(default=False, null=False, blank=True)
    secrecion = models.BooleanField(default=False, null=False, blank=True)
    pigmentacion = models.BooleanField(default=False, null=False, blank=True)
    estrabismo = models.BooleanField(default=False, null=False, blank=True)

    otros_examenes = models.TextField(null=True, blank=True)

    observaciones = models.TextField(null=True, blank=True)

    visio_id = models.OneToOneField(Visiometry, null=False, blank=False, on_delete=models.CASCADE)


class Agudeza(models.Model):
    OPTIONS = (
        ('cerca', 'Cerca'),
        ('lejos', 'Lejos')
    )
    ojo_izquierdo = models.CharField(max_length=10, choices=OPTIONS)
    ojo_derecho = models.CharField(max_length=10, choices=OPTIONS)

    visio_id = models.OneToOneField(Visiometry, null=False, blank=False, on_delete=models.CASCADE)


class Cronomatica(models.Model):
    OPTIONS = (
        ('normal', 'Normal'),
        ('anormal', 'Anormal')
    )
    ojo_izquierdo = models.CharField(max_length=10, choices=OPTIONS)
    ojo_derecho = models.CharField(max_length=10, choices=OPTIONS)

    visio_id = models.OneToOneField(Visiometry, null=False, blank=False, on_delete=models.CASCADE)

