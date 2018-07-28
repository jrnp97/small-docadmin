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
    create_by = models.ForeignKey(DoctorProfile, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.exam_type.name

    class Meta:
        db_table = "exam_audiometria"


class Information(models.Model):
    interpretaciones = models.TextField(null=False, blank=False)
    recomendaciones = models.TextField(null=True, blank=True)

    audiome_id = models.OneToOneField(Audiometry, null=False, blank=False, on_delete=models.CASCADE)


class Otoscopia(models.Model):
    otoscopia_izq = models.FileField()
    otoscopia_der = models.FileField()

    audiome_id = models.OneToOneField(Audiometry, null=False, blank=False, on_delete=models.CASCADE)

