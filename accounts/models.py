""" Models general, only manage user roles and similar models to performance and manage dashboard """
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Base User Class on SM-Laboral only can have 2 roles """
    DOCTOR = 'doctor'
    RECP = 'receptionista'
    LAB = 'p_laboratorio'
    PROFILE_TYPE = (
        (DOCTOR, 'Doctor'),
        (RECP, 'Receptionista'),
        (LAB, 'Personal de Laboratorio'),
    )
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    profile_type = models.CharField(max_length=20, choices=PROFILE_TYPE, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

    def save(self, *args, **kwargs):
        if not self.has_usable_password():
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, **kwargs):
        """ Overwrite method to don't delete user instead change state to deactivate, only delete when is required """
        destroy = kwargs.pop('destroy', False)
        if not destroy:
            self.is_active = False
            self.user.save()
            return 1, dict({'message': 'delete successfully'})
        else:
            return super(User, self).delete(using=using, keep_parents=keep_parents)


# Define user roles
class DoctorProfile(models.Model):
    """ Model to save doctor personal """
    user_id = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, primary_key=True,
                                   related_name='doctor_profile')

    class Meta:
        db_table = 'sm_doctores'


class ReceptionProfile(models.Model):
    """ Model to save receptionist personal """
    user_id = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, primary_key=True,
                                related_name='reception_profile')

    class Meta:
        db_table = 'sm_recepcionistas'


class Laboratorio(models.Model):
    """ Model to describe laboratory binding with sm """
    nombre = models.CharField(max_length=100, null=False, blank=False)
    direccion = models.CharField(max_length=100, null=False, blank=False)
    email_contacto = models.EmailField()

    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, null=False, blank=False,
                                       related_name='laboratorios_registrados')

    class Meta:
        db_table = "laboratorios"


class LaboratoryProfile(models.Model):
    user_id = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, primary_key=True,
                                   related_name='laboratory_profile')
    laboratorio_id = models.ForeignKey(Laboratorio, null=False, blank=False, on_delete=models.CASCADE,
                                       related_name='personal_lab')
    is_admin = models.BooleanField(default=False, null=False, blank=True)

    class Meta:
        db_table = 'personal_labs'

    def save(self, *args, **kwargs):
        """ Overwrite to set default lab profile """
        self.user_id.profile_type = 'p_laboratorio'
        super(LaboratoryProfile, self).save(*args, **kwargs)
