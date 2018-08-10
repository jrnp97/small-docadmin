""" Model to save labs information """
from django.utils import timezone
from django.db import models

from .general import ExamType
from accounts.models import LaboratoryProfile


class Laboratory(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modify = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    exam_type = models.OneToOneField(ExamType,
                                     null=False,
                                     blank=False,
                                     on_delete=models.CASCADE,
                                     related_name='laboratory')
    create_by = models.ForeignKey(LaboratoryProfile,
                                  null=False,
                                  blank=False,
                                  on_delete=models.CASCADE,
                                  related_name='laboratory_forms')

    def __str__(self):
        return "Laboratory"

    def get_exam_type(self):
        return self.exam_type.name

    def get_person(self):
        return self.exam_type.person.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        response = super(Laboratory, self).save(force_insert, force_update, using, update_fields)
        self.exam_type.update_state()
        return response

    class Meta:
        db_table = "laboratory"


class BloodExam(models.Model):
    RH = (
        ('+', 'Positivo'),
        ('-', 'Negativo')
    )

    BLOOD_TYPE = (
        ('a', 'A'),
        ('b-', 'B'),
        ('ab-', 'AB'),
        ('o+', 'O'),
    )
    rh_information = models.CharField(verbose_name='RH', max_length=1, choices=RH, null=False, blank=False)
    blood_type = models.CharField(verbose_name='tipo_sangre', max_length=5, choices=BLOOD_TYPE, null=False,
                                  blank=False)

    laboratory = models.OneToOneField(Laboratory,
                                      null=False,
                                      blank=False,
                                      on_delete=models.CASCADE,
                                      related_name='examen_sangre')


class Exams(models.Model):
        NO_APLICA = 'n'
        APLICA = 'a'
        RESULTS = (
            (NO_APLICA, 'No aplica'),
            (APLICA, 'Aplica'),
        )

        vdrl_date = models.DateField(null=False, blank=False)
        vdrl_lab = models.CharField(max_length=100, null=False, blank=False)
        vdrl_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        serologia_date = models.DateField(null=False, blank=False)
        serologia_lab = models.CharField(max_length=100, null=False, blank=False)
        serologia_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        hemograma_date = models.DateField(null=False, blank=False)
        hemograma_lab = models.CharField(max_length=100, null=False, blank=False)
        hemograma_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        uroanalisis_date = models.DateField(null=False, blank=False)
        uroanalisis_lab = models.CharField(max_length=100, null=False, blank=False)
        uroanalisis_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        colesterol_total_date = models.DateField(null=False, blank=False)
        colesterol_total_lab = models.CharField(max_length=100, null=False, blank=False)
        colesterol_total_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        colesterol_hdi_date = models.DateField(null=False, blank=False)
        colesterol_hdi_lab = models.CharField(max_length=100, null=False, blank=False)
        colesterol_hdi_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        trigliceridos_date = models.DateField(null=False, blank=False)
        trigliceridos_lab = models.CharField(max_length=100, null=False, blank=False)
        trigliceridos_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        colesterol_ldi_date = models.DateField(null=False, blank=False)
        colesterol_ldi_lab = models.CharField(max_length=100, null=False, blank=False)
        colesterol_ldi_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        KOH_unias_date = models.DateField(null=False, blank=False)
        KOH_unias_lab = models.CharField(max_length=100, null=False, blank=False)
        KOH_unias_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        frotis_garganta_date = models.DateField(null=False, blank=False)
        frotis_garganta_lab = models.CharField(max_length=100, null=False, blank=False)
        frotis_garganta_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        coprologico_date = models.DateField(null=False, blank=False)
        coprologico_lab = models.CharField(max_length=100, null=False, blank=False)
        coprologico_result = models.CharField(max_length=1, choices=RESULTS, default=NO_APLICA, null=False, blank=False)

        laboratory = models.OneToOneField(Laboratory,
                                          null=False,
                                          blank=False,
                                          on_delete=models.CASCADE,
                                          related_name='examanes_laboratorios')
