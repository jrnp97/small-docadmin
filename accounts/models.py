""" Models general, only manage user roles and similar models to performance and manage dashboard """
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Base User Class on SM-Laboral only can have 3 roles """
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
    avatar = models.ImageField(upload_to='avatars/user_owner', null=True, blank=True,  default="avatars/default.png")

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
