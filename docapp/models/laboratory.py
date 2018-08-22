""" Model to save labs information
from django.utils import timezone
from django.db import models

from .general import TipoExamen
from accounts.models import LaboratoryProfile


class Laboratory(models.Model):
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)

    tipo_examen = models.OneToOneField(TipoExamen, on_delete=models.PROTECT, related_name='laboratorio')
    registrado_por = models.ForeignKey(LaboratoryProfile, on_delete=models.CASCADE,
                                       related_name='formularios_laboratorios')

    def __str__(self):
        return "Laboratorio"

    def get_exam_type(self):
        return self.tipo_examen.tipo

    def get_person(self):
        return self.tipo_examen.paciente.nombres

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        response = super(Laboratory, self).save(force_insert, force_update, using, update_fields)
        self.tipo_examen.update_state()
        return response

    class Meta:
        db_table = "laboratory"


class ExamenSangre(models.Model):
    RH = (('+', '+'),
          ('-', '-'),)

    TIPOS_DE_SANGRES = (('a', 'A'),
                        ('b-', 'B'),
                        ('o+', 'O'),
                        ('ab-', 'AB'),)

    informacion_rh = models.CharField(verbose_name='RH', max_length=1, choices=RH, null=False, blank=False)
    tipo_de_sangre = models.CharField(max_length=5, choices=TIPOS_DE_SANGRES, null=False,
                                      blank=False)

    laboratory = models.OneToOneField(Laboratory, primary_key=True, on_delete=models.CASCADE,
                                      related_name='examen_sangre')


class Examenes(models.Model):
    nombre_examen = models.CharField(max_length=50, null=False, blank=False)
    fecha = models.DateField(null=True, blank=True)
    nombre_laboratorio = models.CharField(max_length=100, null=True, blank=True)

    laboratory = models.OneToOneField(Laboratory, primary_key=True, on_delete=models.CASCADE, related_name='examen_laboratorio')
"""