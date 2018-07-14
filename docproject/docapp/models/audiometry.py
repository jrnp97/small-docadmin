""" Model to save audiometry form """
from django.db import models
from .general import ExamType, User

""" Questions
Attribute mision

"""


class Audiometry(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modify = models.DateTimeField(null=True, blank=True)
    exam_type = models.OneToOneField(ExamType, on_delete=models.CASCADE)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.exam_type.name


class Information(models.Model):
    interpretaciones = models.TextField(null=False, blank=False)
    recomendaciones = models.TextField(null=True, blank=True)

    audilogy = models.OneToOneField(Audiometry, on_delete=models.CASCADE)


class Otoscopia(models.Model):
    otoscopia_izq = models.FileField()
    otoscopia_der = models.FileField()

    audilogy = models.OneToOneField(Audiometry, on_delete=models.CASCADE)

