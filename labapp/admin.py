from django.contrib import admin
from labapp.models import Laboratorio, LaboratoryProfile, LabExam, ExamResults


admin.site.register(Laboratorio)
admin.site.register(LaboratoryProfile)
admin.site.register(LabExam)
admin.site.register(ExamResults)
