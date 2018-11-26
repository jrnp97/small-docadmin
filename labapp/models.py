from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from accounts.models import ReceptionProfile
from docapp.models import Examinacion

User = get_user_model()


# Create your models here.
class Laboratorio(models.Model):
    """ Model to describe laboratory binding with sm """
    nombre = models.CharField(max_length=100, null=False, blank=False)
    direccion = models.CharField(max_length=100, null=False, blank=False)
    email_contacto = models.EmailField()

    is_active = models.BooleanField(default=True, null=False, blank=True)

    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, null=False, blank=False, related_name='laboratorios')

    class Meta:
        db_table = "laboratorios"

    def __str__(self):
        return self.nombre


class LaboratoryProfile(models.Model):
    """ Model to save laoratory employs """
    user_id = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, primary_key=True,
                                   related_name='laboratory_profile')
    laboratorio_id = models.ForeignKey(Laboratorio, null=False, blank=False, on_delete=models.CASCADE,
                                       related_name='personal_lab')
    is_admin = models.BooleanField(default=False, null=False, blank=True)

    class Meta:
        db_table = 'personal_labs'

    def __str__(self):
        return self.user_id.__str__()


class LabExam(models.Model):
    """ Model to register laboratory exam to do on a patient """
    nombre = models.CharField(max_length=100, null=False, blank=False)

    laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, related_name='procesos')

    examinacion_id = models.ForeignKey(Examinacion, on_delete=models.CASCADE, related_name='examenes_laboratorios')

    registrado_por = models.ForeignKey(ReceptionProfile, null=False, blank=False, on_delete=models.CASCADE,
                                       related_name='examenes_de_labs')

    manejado_por = models.ForeignKey(LaboratoryProfile, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name='examenes')

    def __str__(self):
        return self.nombre

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, update_state=True):
        response = super(LabExam, self).save(force_insert, force_update, using, update_fields)
        if update_state:
            self.examinacion_id.update_lab()
        return response


class ExamResults(models.Model):
    prueba = models.CharField(max_length=200, null=False, blank=False)
    referencias = models.CharField(max_length=200, null=False, blank=False)
    resultados = models.CharField(max_length=200, null=False, blank=False)

    examen = models.ForeignKey(LabExam, null=False, blank=False, on_delete=models.CASCADE, related_name='resultados')
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)

    def __str__(self):
        return self.prueba

