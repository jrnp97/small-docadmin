"""model to save visiometry form"""

from django.db import models
from .general import ExamType, User


class Visiometry(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modify = models.DateTimeField(null=True, blank=True)

    exam_type = models.OneToOneField(ExamType, on_delete=models.CASCADE)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.exam_type.name

    class Meta:
        db_table = "exam_visiometria"


class Sintomas(models.Model):
    ardor = models.BooleanField(default=False, null=False, blank=False)
    dolor = models.BooleanField(default=False, null=False, blank=False)
    cefalea = models.BooleanField(default=False, null=False, blank=False)
    fatiga_visual = models.BooleanField(default=False, null=False, blank=False)
    lagrimeo = models.BooleanField(default=False, null=False, blank=False)
    fotofobia = models.BooleanField(default=False, null=False, blank=False)
    cansansio_lectura = models.BooleanField(default=False, null=False, blank=False)
    prurito = models.BooleanField(default=False, null=False, blank=False)
    lectura_salto_lineas = models.BooleanField(default=False, null=False, blank=False)
    secreciones = models.BooleanField(default=False, null=False, blank=False)
    mala_vision_lejos = models.BooleanField(default=False, null=False, blank=False)
    mala_vision_cerca = models.BooleanField(default=False, null=False, blank=False)

    observaciones = models.TextField(null=True, blank=True)

    visio_id = models.OneToOneField(Visiometry, on_delete=models.CASCADE)

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
    hipertension = models.BooleanField(default=False, null=False, blank=False)
    diabetes = models.BooleanField(default=False, null=False, blank=False)
    colesterol_alto = models.BooleanField(default=False, null=False, blank=False)
    glaucoma = models.BooleanField(default=False, null=False, blank=False)
    migrania = models.BooleanField(default=False, null=False, blank=False)
    catarata = models.BooleanField(default=False, null=False, blank=False)
    cx_ocular = models.BooleanField(default=False, null=False, blank=False)
    trauma = models.BooleanField(default=False, null=False, blank=False)
    cuerpo_extranio = models.BooleanField(default=False, null=False, blank=False)
    hipermetropia = models.BooleanField(default=False, null=False, blank=False)
    miopia = models.BooleanField(default=False, null=False, blank=False)
    astigmatismo = models.BooleanField(default=False, null=False, blank=False)

    # Uso de lentes
    cerca = models.BooleanField(default=False, null=False, blank=False)
    lejos = models.BooleanField(default=False, null=False, blank=False)
    bifocales = models.BooleanField(default=False, null=False, blank=False)
    progresivos = models.BooleanField(default=False, null=False, blank=False)
    contacto = models.BooleanField(default=False, null=False, blank=False)
    oscuros = models.BooleanField(default=False, null=False, blank=False)
    filtro = models.BooleanField(default=False, null=False, blank=False)

    # Examen Externo
    hiperemia = models.BooleanField(default=False, null=False, blank=False)
    pterigion = models.BooleanField(default=False, null=False, blank=False)
    descamacion_parpados = models.BooleanField(default=False, null=False, blank=False)
    secrecion = models.BooleanField(default=False, null=False, blank=False)
    pigmentacion = models.BooleanField(default=False, null=False, blank=False)
    estrabismo = models.BooleanField(default=False, null=False, blank=False)
    otros_examenes = models.TextField()

    observaciones = models.TextField(null=True, blank=True)

    visio_id = models.OneToOneField(Visiometry, on_delete=models.CASCADE)


class Agudeza(models.Model):
    OPTIONS = (
        ('cerca', 'Cerca'),
        ('lejos', 'Lejos')
    )
    ojo_izquierdo = models.CharField(max_length=10, choices=OPTIONS)
    ojo_derecho = models.CharField(max_length=10, choices=OPTIONS)

    visio_id = models.OneToOneField(Visiometry, on_delete=models.CASCADE)


class Cronomatica(models.Model):
    OPTIONS = (
        ('normal', 'Normal'),
        ('anormal', 'Anormal')
    )
    ojo_izquierdo = models.CharField(max_length=10, choices=OPTIONS)
    ojo_derecho = models.CharField(max_length=10, choices=OPTIONS)

    visio_id = models.OneToOneField(Visiometry, on_delete=models.CASCADE)

