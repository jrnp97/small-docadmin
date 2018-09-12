from django.contrib import admin
from labapp.models import Laboratorio, LaboratoryProfile, LabExam, ExamResults
from docapp.models.general import Eps, Afp, Arl


admin.site.register(Laboratorio)
admin.site.register(LaboratoryProfile)
admin.site.register(LabExam)
admin.site.register(ExamResults)
admin.site.register(Eps)
admin.site.register(Afp)
admin.site.register(Arl)

