""" Model to save occupational form"""
from django.utils import timezone
from django.db import models

from .general import ExamType
from accounts.models import DoctorProfile

"""Questions
Section Antecedentes Gineco-Or
Section Columns
"""


class Occupational(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modify = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    exam_type = models.OneToOneField(ExamType,
                                     null=False,
                                     blank=False,
                                     on_delete=models.CASCADE,
                                     related_name='occupational')
    create_by = models.ForeignKey(DoctorProfile,
                                  null=False,
                                  blank=False,
                                  on_delete=models.CASCADE,
                                  related_name='occupational_forms')

    def __str__(self):
        return self.exam_type.name

    class Meta:
        db_table = "exam_ocupacional"


class Ant_familiares(models.Model):
    skin_problems = models.BooleanField(verbose_name="problemas_en_la_piel", default=False, null=False, blank=True)
    epilepsia = models.BooleanField(default=False, null=False, blank=True)
    deafness = models.BooleanField(verbose_name='sordera', default=False, null=False, blank=True)
    nasales = models.BooleanField(default=False, null=False, blank=True)
    oculares = models.BooleanField(default=False, null=False, blank=True)
    respiratorias = models.BooleanField(verbose_name='respiratorias_TBC', default=False, null=False, blank=True)
    cardiacas = models.BooleanField(verbose_name='cardiacas_circulatorias', default=False, null=False, blank=True)
    hernias = models.BooleanField(default=False, null=False, blank=True)
    esqueleticas = models.BooleanField(verbose_name='musculo_esqueleticas', default=False, null=False, blank=True)
    traumaticos = models.BooleanField(verbose_name='fracturas_traumaticos', default=False, null=False, blank=True)
    hematologicas = models.BooleanField(default=False, null=False, blank=True)
    asma = models.BooleanField(verbose_name='alergicas_asma', default=False, null=False, blank=True)
    cancerosas = models.BooleanField(default=False, null=False, blank=True)
    diabeticas = models.BooleanField(default=False, null=False, blank=True)
    hiv = models.BooleanField(verbose_name='HIV', default=False, null=False, blank=True)
    cirugias = models.BooleanField(default=False, null=False, blank=True)
    intoxicaciones = models.BooleanField(default=False, null=False, blank=True)
    otras = models.TextField(verbose_name='otras_enfermedades', null=True, blank=False)

    occupational = models.OneToOneField(Occupational,
                                        null=False,
                                        blank=False,
                                        on_delete=models.CASCADE,
                                        related_name='ant_familiares')


class AntecedentGinecoO(models.Model):
    pass
    occupational = models.OneToOneField(Occupational,
                                        null=False,
                                        blank=False,
                                        on_delete=models.CASCADE,
                                        related_name='ant_gineco')


class Habits(models.Model):
    alcohol = models.BooleanField(default=False)
    drug = models.BooleanField(verbose_name='droga', default=False)
    cigarette = models.BooleanField(verbose_name='cigarrillo', default=False)

    alcohol_abstinence = models.PositiveIntegerField(verbose_name='abstinencia_alcohol', null=True, blank=True)
    drug_abstinence = models.PositiveIntegerField(verbose_name='abstinencia_droga', null=True, blank=True)
    cigarette_abstinence = models.PositiveIntegerField(verbose_name='abstinencia_cigarillo', null=True, blank=True)

    FREQUENCY = (
        ('diaria', 'Diaria'),
        ('semanal', 'Semanal'),
        ('ocacional', 'Ocacional')
    )
    alcohol_frequency = models.CharField(verbose_name='frecuencia_alcohol',
                                         max_length=15, choices=FREQUENCY, null=True, blank=True)

    drug_name = models.CharField(verbose_name='droga_descripcion', max_length=100, null=True, blank=True)
    number_cigarettes = models.PositiveIntegerField(verbose_name='numero_cigarrillos', null=True, blank=True)
    years_cigarette = models.PositiveIntegerField(verbose_name='anios_cigarrillos', null=True, blank=True)

    free_time_actions = models.CharField(max_length=300, verbose_name='tiempo_libre', null=False, blank=False)
    occupational = models.OneToOneField(Occupational,
                                        null=False,
                                        blank=False,
                                        on_delete=models.CASCADE,
                                        related_name='habits')


class FisicoGeneral(models.Model):
    # # General
    genera_look = models.BooleanField(default=False, null=False, blank=True)
    general_nutrition_state = models.BooleanField(default=False, null=False, blank=True)
    general_color_texture = models.BooleanField(default=False, null=False, blank=True)
    general_appearance = models.BooleanField(default=False, null=False, blank=True)
    general_injuries_skin = models.BooleanField(default=False, null=False, blank=True)
    general_irritant_tolerance = models.BooleanField(default=False, null=False, blank=True)
    general_nails = models.BooleanField(default=False, null=False, blank=True)

    occupational = models.OneToOneField(Occupational,
                                        null=False,
                                        blank=False,
                                        on_delete=models.CASCADE,
                                        related_name='fisico_general')


class OrganosSentidos(models.Model):
    # # Senses Organs
    # # # Eyes
    eyes_pupilas = models.BooleanField(verbose_name='conjuntivitis_pupilas_corneas', default=False, null=False, blank=True)
    eyes_deep_vision = models.BooleanField(verbose_name='vision_profunda', default=False, null=False, blank=True)
    eyes_cron_vision = models.BooleanField(verbose_name='vision_cronomatica', default=False, null=False, blank=True)
    eyes_per_vision = models.BooleanField(verbose_name='vision_periferica', default=False, null=False, blank=True)
    eyes_forias = models.BooleanField(default=False, null=False, blank=True)

    # # # Ears
    oidos_pabellones = models.BooleanField(default=False, null=False, blank=True)
    oidos_otoscopia = models.BooleanField(default=False, null=False, blank=True)

    # # # Nose
    nariz_tabique_cornetes = models.BooleanField(default=False, null=False, blank=True)
    nariz_senos_paranasales = models.BooleanField(default=False, null=False, blank=True)

    # # # Mouth
    boca_labios_lengua = models.BooleanField(default=False, null=False, blank=True)
    boca_faringe = models.BooleanField(default=False, null=False, blank=True)
    boca_amigdalas = models.BooleanField(default=False, null=False, blank=True)
    boca_dentadura = models.BooleanField(default=False, null=False, blank=True)

    # # Neck
    cuello_inspect_neck_moves = models.BooleanField(verbose_name='inspecion_cuello_movimientos',
                                             default=False, null=False, blank=True)
    palpacion_cuello_tiroudes = models.BooleanField(default=False, null=False, blank=True)

    # # Torax y pulmones
    pulmones_inspeccion_torax_senos = models.BooleanField(default=False, null=False, blank=True)
    pulmones_palpacion = models.BooleanField(default=False, null=False, blank=True)
    pulmones_auscultacion = models.BooleanField(default=False, null=False, blank=True)

    # # Corazon
    corazon_ritmo = models.BooleanField(default=False, null=False, blank=True)
    corazon_ruidos_cardiacos = models.BooleanField(default=False, null=False, blank=True)
    corazon_circulacion_periferica = models.BooleanField(default=False, null=False, blank=True)

    # # Abdomen
    abdomen_inspeccion = models.BooleanField(default=False, null=False, blank=True)
    abdomen_palpacion_organos = models.BooleanField(default=False, null=False, blank=True)
    abdomen_anillos_inguinales_hernias = models.BooleanField(default=False, null=False, blank=True)

    # # Genito-Unitario
    genito_unitario_riniones = models.BooleanField(default=False, null=False, blank=True)
    genito_unitario_genitales_externos = models.BooleanField(default=False, null=False, blank=True)

    # # Columna
    columna_curvaturas = models.BooleanField(default=False, null=False, blank=True)
    columna_mobilidad = models.BooleanField(default=False, null=False, blank=True)
    columna_tono_musculos_paravertebrales = models.BooleanField(default=False, null=False, blank=True)

    # # Extremidades
    miembros_superiores = models.BooleanField(default=False, null=False, blank=True)
    miembros_inferiores = models.BooleanField(default=False, null=False, blank=True)
    musculos = models.BooleanField(default=False, null=False, blank=True)
    mobilidad_dedos_manos = models.BooleanField(default=False, null=False, blank=True)
    articulaciones = models.BooleanField(default=False, null=False, blank=True)

    # # Neurologico
    esfera_mental = models.BooleanField(default=False, null=False, blank=True)
    sensibilidad_superficial_profunda = models.BooleanField(default=False, null=False, blank=True)
    reflejos = models.BooleanField(default=False, null=False, blank=True)

    otros = models.TextField(null=True, blank=True)

    occupational = models.OneToOneField(Occupational,
                                        null=False,
                                        blank=False,
                                        on_delete=models.CASCADE,
                                        related_name='organos_sistema')


class Conclusion(models.Model):
    STATES = (
        ('apto sin limitaciones', 'Apto Sin Limitaciones'),
        ('apto con limitaciones', 'Apto Con Limitaciones'),
        ('no apto', 'No Apto'),
        ('aplazado', 'Aplazado')
    )

    limitaciones = models.TextField(null=True, blank=True)

    recomendaciones = models.TextField(null=False, blank=False)

    occupational = models.OneToOneField(Occupational,
                                        null=False,
                                        blank=False,
                                        on_delete=models.CASCADE,
                                        related_name='conclusiones')
