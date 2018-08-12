""" Models general """
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    DOCTOR = 'doctor'
    RECP = 'receptionist'
    LAB = 'laboratory'
    PROFILE_TYPE = (
        (DOCTOR, 'Doctor'),
        (RECP, 'Receptionista'),
        (LAB, 'Laboratorio')
    )
    profile_type = models.CharField(max_length=20, choices=PROFILE_TYPE, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

    def save(self, *args, **kwargs):
        if not self.has_usable_password():
            self.set_password(self.password)

        if getattr(self, 'id') is not None:
            try:
                user = User.objects.get(pk=self.id)
            except ObjectDoesNotExist:
                raise SuspiciousOperation(message="User object corrupt.", code='invalid')
            else:
                # Check if profile change
                if user.profile_type != self.profile_type:
                    profile_edit = True
                    # Delete previous profile
                    if user.profile_type == self.DOCTOR:
                        try:
                            DoctorProfile.objects.get(user=user).delete()
                        except IntegrityError or ObjectDoesNotExist:
                            return SuspiciousOperation(message="User profile type corrupt.", code='invalid')
                    elif user.profile_type == self.RECP:
                        try:
                            ReceptionProfile.objects.get(user=user).delete()
                        except IntegrityError or ObjectDoesNotExist:
                            raise SuspiciousOperation(message="User profile type corrupt.", code='invalid')
                    elif user.profile_type == self.LAB:
                        try:
                            LaboratoryProfile.objects.get(user=user).delete()
                        except IntegrityError or ObjectDoesNotExist:
                            raise SuspiciousOperation(message="User profile type corrupt.", code='invalid')

        super(User, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, **kwargs):
        destroy = kwargs.pop('destroy', False)
        if not destroy:
            self.is_active = False
            self.user.save()
            return 1, dict({'message': 'delete successfully'})
        else:
            return super(User, self).delete(using=using, keep_parents=keep_parents)


# Define user roles
class DoctorProfile(models.Model):
    user = models.OneToOneField(User,
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='doctor_profile')
    # Areas
    visiometry = models.BooleanField(default=False, null=False, blank=True)
    audiology = models.BooleanField(default=False, null=False, blank=True)
    audiometry = models.BooleanField(default=False, null=False, blank=True)
    general = models.BooleanField(default=False, null=False, blank=True)

    class Meta:
        db_table = 'doctor_profile'


class ReceptionProfile(models.Model):
    user = models.OneToOneField(User,
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='reception_profile')

    class Meta:
        db_table = 'reception_profile'


class LaboratoryProfile(models.Model):
    user = models.OneToOneField(User,
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='laboratory_profile')

    class Meta:
        db_table = 'laboratory_profile'
