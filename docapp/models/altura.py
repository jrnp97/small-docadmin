from django.db import models
from django.utils import timezone

from docapp.models import Examinacion


class Altura(models.Model):
    examinacion_id = models.OneToOneField(Examinacion, on_delete=models.CASCADE, related_name='altura')

    OPTIONS = (('apto', 'Apto'),
               ('no apto', 'No Apto'))
    conclusion = models.CharField(max_length=20, choices=OPTIONS, null=False, blank=False)

    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)

    def __str__(self):
        return "Altura"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        response = super(Altura, self).save(force_insert, force_update, using, update_fields)
        self.examinacion_id.update_state()
        return response

    class Meta:
        db_table = "exam_altura"


class Questions(models.Model):
    asma = models.BooleanField(default=False, null=False, blank=False)
    dolor_pecho = models.BooleanField(default=False, null=False, blank=False)  # Dolor o presion en el pecho
    palpitaciones_cardiacas_irregulares = models.BooleanField(default=False, null=False, blank=False)
    hipertension_Arterial = models.BooleanField(default=False, null=False, blank=False)
    ataque_cardiaco = models.BooleanField(default=False, null=False, blank=False)
    dolor_espalda = models.BooleanField(default=False, null=False, blank=False)
    convulciones = models.BooleanField(default=False, null=False, blank=False)
    perdida_conocimiento = models.BooleanField(default=False, null=False, blank=False)
    accidente = models.BooleanField(default=False, null=False, blank=False)
    mareos = models.BooleanField(default=False, null=False, blank=False)
    diabetes = models.BooleanField(default=False, null=False, blank=False)
    ayuda_al_realizar_trabajo = models.BooleanField(default=False, null=False, blank=False)
    preocupacion_trabajo_altura = models.BooleanField(default=False, null=False, blank=False)
    problema_psicologico = models.BooleanField(default=False, null=False, blank=False)
    experiencia_en_trabajo_en_altura = models.BooleanField(default=False, null=False, blank=False)

    altura_id = models.ForeignKey(Altura, null=False, blank=False, on_delete=models.CASCADE, related_name='preguntas')
