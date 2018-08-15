"""model to save visiometry form"""
from django.utils import timezone
from django.db import models

from .general import TipoExamen
from accounts.models import DoctorProfile


class Visiometry(models.Model):
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificaco = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)

    tipo_examen = models.OneToOneField(TipoExamen, on_delete=models.CASCADE, related_name='visiometria')
    registrado_por = models.ForeignKey(DoctorProfile, null=False, blank=False, on_delete=models.PROTECT,
                                       related_name='formularios_visiometria')

    def __str__(self):
        return "Visiometria"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        response = super(Visiometry, self).save(force_insert, force_update, using, update_fields)
        self.tipo_examen.update_state()
        return response

    class Meta:
        db_table = "exam_visiometry"


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

    visiometria = models.OneToOneField(Visiometry, on_delete=models.CASCADE, related_name='sintomas')


class AntEnfermedad(models.Model):
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

    observaciones = models.TextField(null=True, blank=True)

    visiometria = models.OneToOneField(Visiometry, on_delete=models.CASCADE, related_name='antecedentes_enfermedades')


class AntUsoLentes(models.Model):
    cerca = models.BooleanField(default=False, null=False, blank=True)
    lejos = models.BooleanField(default=False, null=False, blank=True)
    bifocales = models.BooleanField(default=False, null=False, blank=True)
    progresivos = models.BooleanField(default=False, null=False, blank=True)
    contacto = models.BooleanField(default=False, null=False, blank=True)
    oscuros = models.BooleanField(default=False, null=False, blank=True)
    filtro = models.BooleanField(default=False, null=False, blank=True)

    observaciones = models.TextField(null=True, blank=True)

    visiometria = models.OneToOneField(Visiometry, on_delete=models.CASCADE, related_name='antecedente_uso_lentes')


class AntExamenExterno(models.Model):
    hiperemia = models.BooleanField(default=False, null=False, blank=True)
    pterigion = models.BooleanField(default=False, null=False, blank=True)
    descamacion_parpados = models.BooleanField(default=False, null=False, blank=True)
    secrecion = models.BooleanField(default=False, null=False, blank=True)
    pigmentacion = models.BooleanField(default=False, null=False, blank=True)
    estrabismo = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    visiometria = models.OneToOneField(Visiometry, on_delete=models.CASCADE, related_name='antecedente_examen_externo')


class Agudeza(models.Model):
    OPTIONS = (
        ('cerca', 'Cerca'),
        ('lejos', 'Lejos')
    )
    ojo_izquierdo = models.CharField(max_length=10, choices=OPTIONS)
    ojo_derecho = models.CharField(max_length=10, choices=OPTIONS)

    visiometria = models.OneToOneField(Visiometry, on_delete=models.CASCADE, related_name='agudeza')


class Cronomatica(models.Model):
    OPTIONS = (
        ('normal', 'Normal'),
        ('anormal', 'Anormal')
    )
    ojo_izquierdo = models.CharField(max_length=10, choices=OPTIONS)
    ojo_derecho = models.CharField(max_length=10, choices=OPTIONS)

    visiometria = models.OneToOneField(Visiometry, on_delete=models.CASCADE, related_name='cronomatica')
