from django.contrib import admin

# Register your models here.

from docapp.models import (Company, Person, ExamType, AntecedentJobs, Hazards, JobAccidents,
                           Audiology, Ananmesis, AntecedentesPF, OtrosAntecedentes, Exposiciones, EstadoActual,
                           Visiometry, Sintomas, Antecedentes, Agudeza, Cronomatica,
                           Audiometry, Otoscopia, Information,
                           Occupational, AntecedentPF as AntPF, AntecedentGinecoO, Habits, Exams, ExamPhysic, Conclusion
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


admin.site.register(Company)
admin.site.register(Person)
admin.site.register(ExamType)
admin.site.register(AntecedentJobs, AntJobAdmin)


# Audiology form
class AnanmesisStackInline(admin.StackedInline):
    model = Ananmesis


class AntPFStackInline(admin.StackedInline):
    model = AntecedentesPF


class OtrosAntStackInline(admin.StackedInline):
    model = OtrosAntecedentes


class ExpoStackInline(admin.StackedInline):
    model = Exposiciones


class EstActualAntStackInline(admin.StackedInline):
    model = EstadoActual


class AudiologyAdmin(admin.ModelAdmin):
    model = Audiology
    inlines = (AnanmesisStackInline,
               AntPFStackInline,
               OtrosAntStackInline,
               ExpoStackInline,
               EstActualAntStackInline,)


admin.site.register(Audiology, AudiologyAdmin)


# Visiometry form
class SintomasStackInline(admin.StackedInline):
    model = Sintomas


class AntecedentesStackInline(admin.StackedInline):
    model = Antecedentes
    fieldsets = (
        ('Enfermedad', {'fields': ('hipertension',
                                   'diabetes',
                                   'colesterol_alto',
                                   'glaucoma',
                                   'migrania',
                                   'catarata',
                                   'cx_ocular',
                                   'trauma',
                                   'cuerpo_extranio',
                                   'hipermetropia',
                                   'miopia',
                                   'astigmatismo',)}
         ),
        ('Uso de lentes', {'fields': ('cerca',
                                      'lejos',
                                      'bifocales',
                                      'progresivos',
                                      'contacto',
                                      'oscuros',
                                      'filtro',)}
         ),
        ('Examen Externo', {'fields': ('hiperemia',
                                       'pterigion',
                                       'descamacion_parpados',
                                       'secrecion',
                                       'pigmentacion',
                                       'estrabismo',
                                       'otros_examenes',)}
         )
    )


class AgudezaStackInline(admin.StackedInline):
    model = Agudeza


class CronomaticaStackInline(admin.StackedInline):
    model = Cronomatica


class VisiometryAdmin(admin.ModelAdmin):
    model = Visiometry
    inlines = (SintomasStackInline,
               AntecedentesStackInline,
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


# Occupational form
class AntecedentPFInline(admin.StackedInline):
    model = AntPF


class AntGinInline(admin.StackedInline):
    model = AntecedentGinecoO


class HabitInline(admin.StackedInline):
    model = Habits


class ExamsInline(admin.StackedInline):
    model = Exams


class ExamPhyInline(admin.StackedInline):
    model = ExamPhysic


class ConclusionInline(admin.StackedInline):
    model = Conclusion


class OccupationalAdmin(admin.ModelAdmin):
    model = Occupational
    inlines = (AntecedentPFInline,
               AntGinInline,
               HabitInline,
               ExamsInline,
               ExamPhyInline,
               ConclusionInline,
               )


admin.site.register(Occupational, OccupationalAdmin)
