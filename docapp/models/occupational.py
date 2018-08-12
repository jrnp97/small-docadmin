""" Model to save occupational form"""
from django.utils import timezone
from django.db import models

from .general import TipoExamen
from accounts.models import DoctorProfile


class Occupational(models.Model):
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)

    tipo_examen = models.OneToOneField(TipoExamen, on_delete=models.CASCADE, related_name='occupational')
    registrado_por = models.ForeignKey(DoctorProfile, null=False, blank=False, on_delete=models.PROTECT,
                                       related_name='formulario_ocupacional')

    def __str__(self):
        return self.tipo_examen.tipo

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        response = super(Occupational, self).save(force_insert, force_update, using, update_fields)
        self.tipo_examen.update_state()
        return response

    class Meta:
        db_table = "exam_ocupacional"


class AntPersonalesFamiliares(models.Model):
    problemas_piel = models.BooleanField(default=False, null=False, blank=True)
    epilepsia = models.BooleanField(default=False, null=False, blank=True)
    sordera = models.BooleanField(default=False, null=False, blank=True)
    nasales = models.BooleanField(default=False, null=False, blank=True)
    oculares = models.BooleanField(default=False, null=False, blank=True)
    respiratorias_TBC = models.BooleanField(default=False, null=False, blank=True)
    cardiacas_circulatorias = models.BooleanField(default=False, null=False, blank=True)
    hernias = models.BooleanField(default=False, null=False, blank=True)
    musculo_esqueleticas = models.BooleanField(default=False, null=False, blank=True)
    fracturas_traumaticos = models.BooleanField(default=False, null=False, blank=True)
    hematologicas = models.BooleanField(default=False, null=False, blank=True)
    alergicas_asma = models.BooleanField(default=False, null=False, blank=True)
    cancerosas = models.BooleanField(default=False, null=False, blank=True)
    diabeticas = models.BooleanField(default=False, null=False, blank=True)
    HIV = models.BooleanField(default=False, null=False, blank=True)
    cirugias = models.BooleanField(default=False, null=False, blank=True)
    intoxicaciones = models.BooleanField(default=False, null=False, blank=True)

    observaciones = models.TextField(null=True, blank=True)

    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='antecedentes_personales_familiares')


class AntGinecoObstetricos(models.Model):
    menarquia = models.TextField(null=False, blank=False)
    G = models.PositiveIntegerField(default=0)
    P = models.PositiveIntegerField(default=0)
    A = models.PositiveIntegerField(default=0)
    C = models.PositiveIntegerField(default=0)
    hijos_vivos = models.PositiveIntegerField(default=0)
    FUM = models.DateField(null=False, blank=False)
    ciclos = models.TextField(null=False, blank=False)
    disminorrea = models.BooleanField(default=False, null=False, blank=True)
    FUP = models.DateField(null=True, blank=True)
    clase = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='antecedente_gineco_obstetricos')


# Habitos Opciones
class HabitoAlcohol(models.Model):
    alcohol = models.BooleanField(default=False)
    tiempo_de_abstinencia = models.PositiveIntegerField(null=True, blank=True)
    FRECUENCIA = (('diaria', 'Diaria'),
                  ('semanal', 'Semanal'),
                  ('ocacional', 'Ocacional'),)
    frecuencia = models.CharField(max_length=15, choices=FRECUENCIA, null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='habito_alcohol')


class HabitoDroga(models.Model):
    droga = models.BooleanField(default=False)
    tiempo_de_abstinencia = models.PositiveIntegerField(null=True, blank=True)
    descripcion = models.CharField(verbose_name='droga_descripcion', max_length=100, null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='habito_droga')


class HabitoCigarrillo(models.Model):
    cigarette = models.BooleanField(verbose_name='cigarrillo', default=False)
    tiempo_de_abstinencia = models.PositiveIntegerField(null=True, blank=True)
    numbero_diarios = models.PositiveIntegerField(null=True, blank=True)
    anios = models.PositiveIntegerField(verbose_name='años', null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='habito_cigarillo')


class HabitoGenerales(models.Model):
    acciones_en_tiempo_libre = models.CharField(max_length=300, verbose_name='tiempo_libre', null=False, blank=False)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='habito_general')


# Examane Fisico Organo O Sistema
"""
# TODO Seccion BIOMETRIA !!!
"""
class ExamFisicoAspectoGeneral(models.Model):
    # # General
    apariencia_general = models.BooleanField(default=False, null=False, blank=True)
    estado_de_nutricion = models.BooleanField(default=False, null=False, blank=True)
    color_y_textura = models.BooleanField(default=False, null=False, blank=True)
    aspecto = models.BooleanField(default=False, null=False, blank=True)
    lesiones_de_piel = models.BooleanField(default=False, null=False, blank=True)
    tolerancia_irritantes = models.BooleanField(default=False, null=False, blank=True)
    unias = models.BooleanField(verbose_name='uñas', default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_aspecto_general')


class ExamFisicoOjos(models.Model):
    pupilas_conjuntivas_corneas = models.BooleanField(default=False, null=False, blank=True)
    vision_profundidad = models.BooleanField(default=False, null=False, blank=True)
    vision_cronomatica = models.BooleanField(default=False, null=False, blank=True)
    vision_periferica = models.BooleanField(default=False, null=False, blank=True)
    forias = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_ojos')


class ExamFisicoOidos(models.Model):
    pabellones = models.BooleanField(default=False, null=False, blank=True)
    otoscopia = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_oidos')


class ExamFisicoNariz(models.Model):
    tabique_cornetes = models.BooleanField(default=False, null=False, blank=True)
    senos_paranasales = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_nariz')


class ExamFisicoBoca(models.Model):
    faringe = models.BooleanField(default=False, null=False, blank=True)
    amigdalas = models.BooleanField(default=False, null=False, blank=True)
    dentadura = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_boca')


class ExamFisicoCuello(models.Model):
    movimientos = models.BooleanField(default=False, null=False, blank=True)
    palpacion = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_cuello')


class ExamFisicoToraxPulmones(models.Model):
    inspeccion = models.BooleanField(default=False, null=False, blank=True)
    palpacion = models.BooleanField(default=False, null=False, blank=True)
    auscultacion = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_torax_pulmones')


class ExamFisicoCorazon(models.Model):
    ritmo = models.BooleanField(default=False, null=False, blank=True)
    ruidos_cardiacos = models.BooleanField(default=False, null=False, blank=True)
    circularion_periferica = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_corazon')


class ExamFisicoAbdomen(models.Model):
    inspeccion = models.BooleanField(default=False, null=False, blank=True)
    papacion_organos = models.BooleanField(default=False, null=False, blank=True)
    anillos_inguinales = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_abdomen')


class ExamFisicoGenitoUnitario(models.Model):
    riniones = models.BooleanField(verbose_name='riñones', default=False, null=False, blank=True)
    genitales_externos = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_genito_unitario')


class ExamFisicoColumna(models.Model):
    curvaturas = models.BooleanField(default=False, null=False, blank=True)
    movilidad = models.BooleanField(default=False, null=False, blank=True)
    tono_musculos_paravertebrales = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_columna')


class ExamFisicoExtremidades(models.Model):
    movilidad_miembros_superioes = models.BooleanField(default=False, null=False, blank=True)
    movilidad_miembros_inferiore = models.BooleanField(default=False, null=False, blank=True)
    musculos = models.BooleanField(default=False, null=False, blank=True)
    movilidad_dedos_manos = models.BooleanField(default=False, null=False, blank=True)
    articulaciones = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_extremidades')


class ExamFisicoNeurologico(models.Model):
    esfera_mental = models.BooleanField(default=False, null=False, blank=True)
    sensibilidad_superficial = models.BooleanField(default=False, null=False, blank=True)
    sensibilidad_profunda = models.BooleanField(default=False, null=False, blank=True)
    reflejos = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='examen_fisico_neurologico')


"""
# TODO SECCION COLUMNA !!!!!
"""


class Conclusion(models.Model):
    ESTADOS = (('apto sin limitaciones', 'Apto Sin Limitaciones'),
               ('apto con limitaciones', 'Apto Con Limitaciones'),
               ('no apto', 'No Apto'),
               ('aplazado', 'Aplazado'),)
    estado = models.CharField(max_length=30, choices=ESTADOS, null=False, blank=False)
    limitaciones = models.TextField(null=True, blank=True)
    recomendaciones = models.TextField(null=False, blank=False)

    occupational = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                        related_name='conclusiones')
