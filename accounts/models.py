""" Models general """
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    DOCTOR = 'doctor'
    RECP = 'receptionist'
    LAB = 'laboratory'
    PROFILE_TYPE = (
        (DOCTOR, 'Doctor'),
        (RECP, 'Receptionist'),
        (LAB, 'Laboratory')
    )
    profile_type = models.CharField(max_length=20, choices=PROFILE_TYPE, null=False, blank=False)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

    def delete(self, using=None, keep_parents=False):
        super(User, self).delete(using, keep_parents)

    def save(self, *args, **kwargs):
        if not self.has_usable_password():
            self.set_password(self.password)

        # If request is to update info
        profile_edit = False
        exist_user = False
        if getattr(self, 'id') is not None:
            try:
                user = User.objects.get(pk=self.id)
            except ObjectDoesNotExist:
                raise ValidationError(message="User object corrupt.", code='invalid')
            else:
                exist_user = True
                # Check if profile change
                if user.profile_type != self.profile_type:
                    profile_edit = True
                    # Delete previous profile
                    if user.profile_type == self.DOCTOR:
                        try:
                            DoctorProfile.objects.get(user=user).delete()
                        except IntegrityError or ObjectDoesNotExist:
                            return ValidationError(message="User profile type corrupt.", code='invalid')
                    elif user.profile_type == self.RECP:
                        try:
                            ReceptionProfile.objects.get(user=user).delete()
                        except IntegrityError or ObjectDoesNotExist:
                            return ValidationError(message="User profile type corrupt.", code='invalid')
                    elif user.profile_type == self.LAB:
                        try:
                            LaboratoryProfile.objects.get(user=user).delete()
                        except IntegrityError or ObjectDoesNotExist:
                            return ValidationError(message="User profile type corrupt.", code='invalid')

        super(User, self).save(*args, **kwargs)

        if profile_edit or not exist_user:
            # Save user profile
            if self.profile_type == self.DOCTOR:
                try:
                    DoctorProfile.objects.create(user=self)
                except IntegrityError:
                    return ValidationError("User profile don't save contact admin")
            elif self.profile_type == self.RECP:
                try:
                    ReceptionProfile.objects.create(user=self)
                except IntegrityError:
                    return ValidationError("User profile don't save contact admin")
            elif self.profile_type == self.LAB:
                try:
                    LaboratoryProfile.objects.create(user=self)
                except IntegrityError:
                    return ValidationError("User profile don't save contact admin")


# Define user roles
class DoctorProfile(models.Model):
    user = models.OneToOneField(User,
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='doctor_profile')
    # Areas
    visiometra = models.BooleanField(default=False, null=False, blank=True)
    audiologo = models.BooleanField(default=False, null=False, blank=True)
    audiometra = models.BooleanField(default=False, null=False, blank=True)
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
