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
    exam_type = models.OneToOneField(ExamType, null=False, blank=False, on_delete=models.CASCADE)
    create_by = models.ForeignKey(DoctorProfile,
                                  null=False,
                                  blank=False,
                                  on_delete=models.CASCADE,
                                  related_name='occupational_forms')

    def __str__(self):
        return self.exam_type.name

    class Meta:
        db_table = "exam_ocupacional"


class AntecedentPF(models.Model):
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

    occupa_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE)


class AntecedentGinecoO(models.Model):
    pass
    occupa_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE)


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
    occupa_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE)


class ExamPhysic(models.Model):
    # Biometrics(models.Model):

    # OrganSystem
    # # General
    genera_look = models.BooleanField(default=False, null=False, blank=True)
    nutrition_state = models.BooleanField(default=False, null=False, blank=True)
    color_texture = models.BooleanField(default=False, null=False, blank=True)
    appearance = models.BooleanField(default=False, null=False, blank=True)
    injuries_skin = models.BooleanField(default=False, null=False, blank=True)
    irritant_tolerance = models.BooleanField(default=False, null=False, blank=True)
    nails = models.BooleanField(default=False, null=False, blank=True)

    # # Senses Organs

    # # # Eyes
    pupilas = models.BooleanField(verbose_name='conjuntivitis_pupilas_corneas', default=False, null=False, blank=True)
    deep_vision = models.BooleanField(verbose_name='vision_profunda', default=False, null=False, blank=True)
    cron_vision = models.BooleanField(verbose_name='vision_cronomatica', default=False, null=False, blank=True)
    per_vision = models.BooleanField(verbose_name='vision_periferica', default=False, null=False, blank=True)
    forias = models.BooleanField(default=False, null=False, blank=True)

    # # # Ears
    pabellones = models.BooleanField(default=False, null=False, blank=True)
    otoscopia = models.BooleanField(default=False, null=False, blank=True)

    # # # Nose
    tabique_cornetes = models.BooleanField(default=False, null=False, blank=True)
    senos_paranasales = models.BooleanField(default=False, null=False, blank=True)

    # # # Mouth
    labios_lengua = models.BooleanField(default=False, null=False, blank=True)
    faringe = models.BooleanField(default=False, null=False, blank=True)
    amigdalas = models.BooleanField(default=False, null=False, blank=True)
    dentadura = models.BooleanField(default=False, null=False, blank=True)

    # # Neck
    inspect_neck_moves = models.BooleanField(verbose_name='inspecion_cuello_movimientos',
                                             default=False, null=False, blank=True)
    palpacion_cuello_tiroudes = models.BooleanField(default=False, null=False, blank=True)

    # # Torax y pulmones
    inspeccion_torax_senos = models.BooleanField(default=False, null=False, blank=True)
    palpacion = models.BooleanField(default=False, null=False, blank=True)
    auscultacion = models.BooleanField(default=False, null=False, blank=True)

    # # Corazon
    ritmo = models.BooleanField(default=False, null=False, blank=True)
    ruidos_cardiacos = models.BooleanField(default=False, null=False, blank=True)
    circulacion_periferica = models.BooleanField(default=False, null=False, blank=True)

    # # Abdomen
    inspeccion = models.BooleanField(default=False, null=False, blank=True)
    palpacion_organos = models.BooleanField(default=False, null=False, blank=True)
    anillos_inguinales_hernias = models.BooleanField(default=False, null=False, blank=True)

    # # Genito-Unitario
    riniones = models.BooleanField(default=False, null=False, blank=True)
    genitales_externos = models.BooleanField(default=False, null=False, blank=True)

    # # Columna
    curvaturas = models.BooleanField(default=False, null=False, blank=True)
    mobilidad = models.BooleanField(default=False, null=False, blank=True)
    tono_musculos_paravertebrales = models.BooleanField(default=False, null=False, blank=True)

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

    occupa_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE)

    # Column


class Conclusion(models.Model):
    STATES = (
        ('apto sin limitaciones', 'Apto Sin Limitaciones'),
        ('apto con limitaciones', 'Apto Con Limitaciones'),
        ('no apto', 'No Apto'),
        ('aplazado', 'Aplazado')
    )

    limitaciones = models.TextField(null=True, blank=True)

    recomendaciones = models.TextField(null=False, blank=False)

    occupa_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE)
