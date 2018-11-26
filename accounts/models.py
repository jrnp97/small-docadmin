""" Models general, only manage user roles and similar models to performance and manage dashboard """
from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.choices import PROFILE_TYPE


class User(AbstractUser):
    """ Base User Class on SM-Laboral only can have 3 roles """
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
            self.save()
            return 1, dict({'message': 'delete successfully'})
        else:
            return super(User, self).delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_profile(self):
        if hasattr(self, 'doctor_profile'):
            return 'doctor_profile'
        elif hasattr(self, 'reception_profile'):
            return 'reception_profile'
        elif hasattr(self, 'laboratory_profile'):
            return 'laboratory_profile'


# Define user roles
class DoctorProfile(models.Model):
    """ Model to save doctor personal """
    user_id = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, primary_key=True,
                                   related_name='doctor_profile')

    class Meta:
        db_table = 'sm_doctores'

    def __str__(self):
        return self.user_id.get_full_name()


class ReceptionProfile(models.Model):
    """ Model to save receptionist personal """
    user_id = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, primary_key=True,
                                   related_name='reception_profile')

    class Meta:
        db_table = 'sm_recepcionistas'

    def __str__(self):
        return self.user_id.get_full_name()
