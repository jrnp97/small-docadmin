""" Model to save audiometry form """
from django.utils import timezone
from django.db import models

from .general import ExamType
from accounts.models import DoctorProfile

""" Questions
Attribute mision

"""


class Audiometry(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modify = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    exam_type = models.OneToOneField(ExamType, null=False, blank=False, on_delete=models.CASCADE)
    create_by = models.ForeignKey(DoctorProfile,
                                  null=False,
                                  blank=False,
                                  on_delete=models.CASCADE,
                                  related_name='audiometry_forms')

    def __str__(self):
        return self.exam_type.name

    class Meta:
        db_table = "exam_audiometria"


class Information(models.Model):
    interpretaciones = models.TextField(null=False, blank=False)
    recomendaciones = models.TextField(null=True, blank=True)

    audiometry = models.OneToOneField(Audiometry, null=False, blank=False,
                                      on_delete=models.CASCADE, related_name='informacion')


class Otoscopia(models.Model):
    otoscopia_izq = models.ImageField(upload_to='otoscopia/%Y/%m/%d/')
    otoscopia_der = models.ImageField(upload_to='otoscopia/%Y/%m/%d/')

    audiometry = models.OneToOneField(Audiometry, null=False,
                                      blank=False,
                                      on_delete=models.CASCADE,
                                      related_name='otoscopia')
