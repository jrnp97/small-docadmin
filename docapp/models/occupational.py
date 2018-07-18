""" Model to save occupational form"""
from django.db import models
from .general import ExamType, User

"""Questions
Section Antecedentes Gineco-Or
Section Columns
"""


class Occupational(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modify = models.DateTimeField(null=True, blank=True)

    exam_type = models.OneToOneField(ExamType, on_delete=models.CASCADE)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.exam_type.name

    class Meta:
        db_table = "exam_ocupacional"


class AntecedentPF(models.Model):
    skin_problems = models.BooleanField(verbose_name="problemas_en_la_piel", default=False, null=False, blank=False)
    epilepsia = models.BooleanField(default=False, null=False, blank=False)
    deafness = models.BooleanField(verbose_name='sordera', default=False, null=False, blank=False)
    nasales = models.BooleanField(default=False, null=False, blank=False)
    oculares = models.BooleanField(default=False, null=False, blank=False)
    respiratorias = models.BooleanField(verbose_name='respiratorias_TBC', default=False, null=False, blank=False)
    cardiacas = models.BooleanField(verbose_name='cardiacas_circulatorias', default=False, null=False, blank=False)
    hernias = models.BooleanField(default=False, null=False, blank=False)
    esqueleticas = models.BooleanField(verbose_name='musculo_esqueleticas', default=False, null=False, blank=False)
    traumaticos = models.BooleanField(verbose_name='fracturas_traumaticos', default=False, null=False, blank=False)
    hematologicas = models.BooleanField(default=False, null=False, blank=False)
    asma = models.BooleanField(verbose_name='alergicas_asma', default=False, null=False, blank=False)
    cancerosas = models.BooleanField(default=False, null=False, blank=False)
    diabeticas = models.BooleanField(default=False, null=False, blank=False)
    hiv = models.BooleanField(verbose_name='HIV', default=False, null=False, blank=False)
    cirugias = models.BooleanField(default=False, null=False, blank=False)
    intoxicaciones = models.BooleanField(default=False, null=False, blank=False)
    otras = models.TextField(verbose_name='otras_enfermedades', null=True, blank=False)

    occupational = models.OneToOneField(Occupational, on_delete=models.CASCADE)


class AntecedentGinecoO(models.Model):
    pass
    occupational = models.OneToOneField(Occupational, on_delete=models.CASCADE)


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
    occupational = models.OneToOneField(Occupational, on_delete=models.CASCADE)


class Exams(models.Model):
    RESULTS = (
        ('n', 'No aplica'),
        ('a', 'Aplica'),
    )

    vdrl_date = models.DateField(null=False, blank=False)
    vdrl_lab = models.CharField(max_length=100, null=False, blank=False)
    vdrl_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    serologia_date = models.DateField(null=False, blank=False)
    serologia_lab = models.CharField(max_length=100, null=False, blank=False)
    serologia_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    hemograma_date = models.DateField(null=False, blank=False)
    hemograma_lab = models.CharField(max_length=100, null=False, blank=False)
    hemograma_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    uroanalisis_date = models.DateField(null=False, blank=False)
    uroanalisis_lab = models.CharField(max_length=100, null=False, blank=False)
    uroanalisis_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    colesterol_total_date = models.DateField(null=False, blank=False)
    colesterol_total_lab = models.CharField(max_length=100, null=False, blank=False)
    colesterol_total_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    colesterol_hdi_date = models.DateField(null=False, blank=False)
    colesterol_hdi_lab = models.CharField(max_length=100, null=False, blank=False)
    colesterol_hdi_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    trigliceridos_date = models.DateField(null=False, blank=False)
    trigliceridos_lab = models.CharField(max_length=100, null=False, blank=False)
    trigliceridos_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    colesterol_ldi_date = models.DateField(null=False, blank=False)
    colesterol_ldi_lab = models.CharField(max_length=100, null=False, blank=False)
    colesterol_ldi_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    KOH_unias_date = models.DateField(null=False, blank=False)
    KOH_unias_lab = models.CharField(max_length=100, null=False, blank=False)
    KOH_unias_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    frotis_garganta_date = models.DateField(null=False, blank=False)
    frotis_garganta_lab = models.CharField(max_length=100, null=False, blank=False)
    frotis_garganta_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    coprologico_date = models.DateField(null=False, blank=False)
    coprologico_lab = models.CharField(max_length=100, null=False, blank=False)
    coprologico_result = models.CharField(max_length=1, choices=RESULTS, default='n', null=False, blank=False)

    RH = (
        ('+', 'Positivo'),
        ('-', 'Negativo')
    )

    BLOOD_TYPE = (
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-')
    )
    rh_information = models.CharField(verbose_name='RH', max_length=1, choices=RH, null=False, blank=False)
    blood_type = models.CharField(verbose_name='tipo_sangre', max_length=5, choices=BLOOD_TYPE, null=False, blank=False)

    occupational = models.OneToOneField(Occupational, on_delete=models.CASCADE)


class ExamPhysic(models.Model):
    # Biometrics(models.Model):

    # OrganSystem
    # # General
    genera_look = models.BooleanField(default=False, null=False, blank=False)
    nutrition_state = models.BooleanField(default=False, null=False, blank=False)
    color_texture = models.BooleanField(default=False, null=False, blank=False)
    appearance = models.BooleanField(default=False, null=False, blank=False)
    injuries_skin = models.BooleanField(default=False, null=False, blank=False)
    irritant_tolerance = models.BooleanField(default=False, null=False, blank=False)
    nails = models.BooleanField(default=False, null=False, blank=False)

    # # Senses Organs

    # # # Eyes
    pupilas = models.BooleanField(verbose_name='conjuntivitis_pupilas_corneas', default=False, null=False, blank=False)
    deep_vision = models.BooleanField(verbose_name='vision_profunda', default=False, null=False, blank=False)
    cron_vision = models.BooleanField(verbose_name='vision_cronomatica', default=False, null=False, blank=False)
    per_vision = models.BooleanField(verbose_name='vision_periferica', default=False, null=False, blank=False)
    forias = models.BooleanField(default=False, null=False, blank=False)

    # # # Ears
    pabellones = models.BooleanField(default=False, null=False, blank=False)
    otoscopia = models.BooleanField(default=False, null=False, blank=False)

    # # # Nose
    tabique_cornetes = models.BooleanField(default=False, null=False, blank=False)
    senos_paranasales = models.BooleanField(default=False, null=False, blank=False)

    # # # Mouth
    labios_lengua = models.BooleanField(default=False, null=False, blank=False)
    faringe = models.BooleanField(default=False, null=False, blank=False)
    amigdalas = models.BooleanField(default=False, null=False, blank=False)
    dentadura = models.BooleanField(default=False, null=False, blank=False)

    # # Neck
    inspect_neck_moves = models.BooleanField(verbose_name='inspecion_cuello_movimientos',
                                             default=False, null=False, blank=False)
    palpacion_cuello_tiroudes = models.BooleanField(default=False, null=False, blank=False)

    # # Torax y pulmones
    inspeccion_torax_senos = models.BooleanField(default=False, null=False, blank=False)
    palpacion = models.BooleanField(default=False, null=False, blank=False)
    auscultacion = models.BooleanField(default=False, null=False, blank=False)

    # # Corazon
    ritmo = models.BooleanField(default=False, null=False, blank=False)
    ruidos_cardiacos = models.BooleanField(default=False, null=False, blank=False)
    circulacion_periferica = models.BooleanField(default=False, null=False, blank=False)

    # # Abdomen
    inspeccion = models.BooleanField(default=False, null=False, blank=False)
    palpacion_organos = models.BooleanField(default=False, null=False, blank=False)
    anillos_inguinales_hernias = models.BooleanField(default=False, null=False, blank=False)

    # # Genito-Unitario
    riniones = models.BooleanField(default=False, null=False, blank=False)
    genitales_externos = models.BooleanField(default=False, null=False, blank=False)

    # # Columna
    curvaturas = models.BooleanField(default=False, null=False, blank=False)
    mobilidad = models.BooleanField(default=False, null=False, blank=False)
    tono_musculos_paravertebrales = models.BooleanField(default=False, null=False, blank=False)

    # # Extremidades
    miembros_superiores = models.BooleanField(default=False, null=False, blank=False)
    miembros_inferiores = models.BooleanField(default=False, null=False, blank=False)
    musculos = models.BooleanField(default=False, null=False, blank=False)
    mobilidad_dedos_manos = models.BooleanField(default=False, null=False, blank=False)
    articulaciones = models.BooleanField(default=False, null=False, blank=False)

    # # Neurologico
    esfera_mental = models.BooleanField(default=False, null=False, blank=False)
    sensibilidad_superficial_profunda = models.BooleanField(default=False, null=False, blank=False)
    reflejos = models.BooleanField(default=False, null=False, blank=False)

    otros = models.TextField(null=True, blank=True)

    occupational = models.OneToOneField(Occupational, on_delete=models.CASCADE)

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

    occupational = models.OneToOneField(Occupational, on_delete=models.CASCADE)
