from django.contrib import admin

from docapp.models import Otoscopia

admin.site.register(Otoscopia)
"""
# Register your models here.

from docapp.models import (Company, Person, ExamType, AntecedentJobs, Hazards, JobAccidents,
                           Audiology, Ananmesis, AntecedentesPF, Exposiciones, EstadoActual,
                           Visiometry, Sintomas, Agudeza, Cronomatica,
                           Audiometry, Otoscopia, Information,
                           Occupational, AntecedentPF as AntPF, AntecedentGinecoO, Habits, ExamPhysic, Conclusion
                           )

# General information


class HazarStackInline(admin.StackedInline):
    model = Hazards


class JobAcStackInline(admin.StackedInline):
    model = JobAccidents
    extra = 1


class AntJobAdmin(admin.ModelAdmin):
    model = AntecedentJobs
    inlines = (HazarStackInline,
               JobAcStackInline,
               )
    list_display = ('__str__', 'company', 'occupation', )


# Make person exam
class ExamTypeAdmin(admin.ModelAdmin):
    model = ExamType
    list_display = ('name', 'person', 'create_date')


admin.site.register(Company)
admin.site.register(Person)
admin.site.register(ExamType, ExamTypeAdmin)
admin.site.register(AntecedentJobs, AntJobAdmin)


# Audiology form
class AnanmesisStackInline(admin.StackedInline):
    model = Ananmesis


class AntPFStackInline(admin.StackedInline):
    model = AntecedentesPF


class ExpoStackInline(admin.StackedInline):
    model = Exposiciones


class EstActualAntStackInline(admin.StackedInline):
    model = EstadoActual


class AudiologyAdmin(admin.ModelAdmin):
    model = Audiology
    inlines = (AnanmesisStackInline,
               AntPFStackInline,
               ExpoStackInline,
               EstActualAntStackInline,)
    list_display = ('get_exam_type', 'get_person', 'create_by', 'last_modify')


admin.site.register(Audiology, AudiologyAdmin)


# Visiometry form
class SintomasStackInline(admin.StackedInline):
    model = Sintomas


class AgudezaStackInline(admin.StackedInline):
    model = Agudeza


class CronomaticaStackInline(admin.StackedInline):
    model = Cronomatica


class VisiometryAdmin(admin.ModelAdmin):
    model = Visiometry
    inlines = (SintomasStackInline,
               AgudezaStackInline,
               CronomaticaStackInline,
               )


admin.site.register(Visiometry, VisiometryAdmin)


# Audiometry form
class InformationStackInline(admin.StackedInline):
    model = Information


class OtoscopiaStackInline(admin.StackedInline):
    model = Otoscopia


class AudiometryAdmin(admin.ModelAdmin):
    model = Audiometry
    inlines = (OtoscopiaStackInline,
               InformationStackInline,
               )


admin.site.register(Audiometry, AudiometryAdmin)


# Occupationatl form
class AntecedentPFInline(admin.StackedInline):
    model = AntPF


class AntGinInline(admin.StackedInline):
    model = AntecedentGinecoO


class HabitInline(admin.StackedInline):
    model = Habits


class ExamPhyInline(admin.StackedInline):
    model = ExamPhysic


class ConclusionInline(admin.StackedInline):
    model = Conclusion


class OccupationalAdmin(admin.ModelAdmin):
    model = Occupational
    inlines = (AntecedentPFInline,
               AntGinInline,
               HabitInline,
               ExamPhyInline,
               ConclusionInline,
               )


admin.site.register(Occupational, OccupationalAdmin)
"""