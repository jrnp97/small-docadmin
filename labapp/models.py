from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from accounts.models import ReceptionProfile

User = get_user_model()


# Create your models here.
class Laboratorio(models.Model):
    """ Model to describe laboratory binding with sm """
    nombre = models.CharField(max_length=100, null=False, blank=False)
    direccion = models.CharField(max_length=100, null=False, blank=False)
    email_contacto = models.EmailField()

    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, null=False, blank=False,
                                       related_name='laboratorios')

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
        return self.user_id


class LabExam(models.Model):
    """ Model to register laboratory exam to do on a patient """
    nombre = models.CharField(max_length=50, null=False, blank=False)

    laboratorio_id = models.ForeignKey(Laboratorio, null=True, blank=True, on_delete=models.CASCADE,
                                       related_name='procesos')
    registrado_por = models.ForeignKey(ReceptionProfile, null=False, blank=False, on_delete=models.CASCADE,
                                       related_name='examenes_de_labs')
    manejado_por = models.OneToOneField(LaboratoryProfile, null=True, blank=True, on_delete=models.CASCADE,
                                        related_name='examenes')

    def __str__(self):
        return self.nombre


class ExamResults(models.Model):
    prueba = models.CharField(max_length=200, null=False, blank=False)
    referencias = models.CharField(max_length=200, null=False, blank=False)
    resultados = models.CharField(max_length=200, null=False, blank=False)

    examen = models.ForeignKey(LabExam, null=False, blank=False, on_delete=models.CASCADE, related_name='resultados')
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
