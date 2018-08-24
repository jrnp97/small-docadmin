""" Model to save occupational form"""
from django.utils import timezone
from django.db import models

from .general import Examinacion


class Occupational(models.Model):
    examinacion_id = models.OneToOneField(Examinacion, on_delete=models.CASCADE, related_name='ocupacional')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)

    def __str__(self):
        return self.examinacion_id.tipo

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        response = super(Occupational, self).save(force_insert, force_update, using, update_fields)
        self.examinacion_id.update_state()
        return response

    class Meta:
        db_table = "exam_ocupacional"


class AntPersonalesFamiliares(models.Model):
    """ To check if a paciente have Antecedent from family or personal default (no present)"""
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

    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='antecedentes_personales_familiares')


class AntGinecoObstetricos(models.Model):
    """ Section to describe a women state (only show when pacient is women) """
    menarquia = models.TextField(default='NA', null=False, blank=False)
    ultima_gestacion = models.PositiveIntegerField(default=0)
    numero_de_partos = models.PositiveIntegerField(default=0)
    numero_de_abortos = models.PositiveIntegerField(default=0)
    numero_de_cesarias = models.PositiveIntegerField(default=0)
    hijos_vivos = models.PositiveIntegerField(default=0)
    fecha_ultima_mestruacion = models.DateField(default='00/00/0000', null=False, blank=False)
    clase_mestruacion = models.TextField(null=True, blank=True)
    ciclos = models.TextField(default='NA', null=False, blank=False)
    disminorrea = models.BooleanField(default=False, null=False, blank=True)
    fecha_ultimo_parto = models.DateField(null=True, blank=True)

    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='antecedente_gineco_obstetricos')


# Habitos Opciones
class HabitoAlcohol(models.Model):
    aplica = models.BooleanField(default=False, null=False, blank=True)
    tiempo_de_abstinencia = models.PositiveIntegerField(null=True, blank=True)
    FRECUENCIA = (('diaria', 'Diaria'),
                  ('semanal', 'Semanal'),
                  ('ocacional', 'Ocacional'),)
    frecuencia = models.CharField(max_length=15, choices=FRECUENCIA, null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='habito_alcohol')


class HabitoDroga(models.Model):
    aplica = models.BooleanField(default=False, null=False, blank=True)
    tiempo_de_abstinencia = models.PositiveIntegerField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='habito_droga')


class HabitoCigarrillo(models.Model):
    aplica = models.BooleanField(default=False, null=False, blank=True)
    tiempo_de_abstinencia = models.PositiveIntegerField(null=True, blank=True)
    numero_de_cigarillos_diarios = models.PositiveIntegerField(null=True, blank=True)
    anios = models.PositiveIntegerField(verbose_name='años', null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='habito_cigarillo')


class HabitoGenerales(models.Model):
    deportes = models.TextField(null=False, blank=False)
    frecuencia = models.PositiveIntegerField()
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='habito_general')


class RevisionSistemas(models.Model):
    enfermedad_actual = models.BooleanField(default=False, null=False, blank=True)
    descripcion = models.TextField(default='No Presenta', null=False, blank=True)
    ocupacional_id = models.ForeignKey(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                       related_name='revision_por_sistemas')


# Examane Fisico Organo O Sistema
class Biometria(models.Model):
    """ Model to save biometry information (answer - What's T.A) """
    BIOTIPO = (('pequeño', 'Pequeño'),
               ('mediano', 'Mediano'),
               ('grande', 'Grande'))
    biotipo = models.CharField(max_length=10, choices=BIOTIPO, null=False, blank=False)
    peso_en_KG = models.PositiveIntegerField(null=False, blank=False)
    talla_en_CM = models.PositiveIntegerField(null=False, blank=False)
    MOVIMIENTO = (('diestro', 'Diestro'),
                  ('zurdo', 'Zurdo'),
                  ('ambidiestro', 'Ambidiestro'))
    cuerpo_dominio = models.CharField(max_length=15, choices=MOVIMIENTO, default='diestro', null=False, blank=False)
    frecuencia_cardiaca = models.PositiveIntegerField(null=False, blank=False)
    frecuencia_respiratoria = models.PositiveIntegerField(null=False, blank=False)
    indice_de_masa_corporal = models.FloatField(null=True, blank=True, editable=False)  # Auto calculate

    ocupacional_id = models.ForeignKey(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                       related_name='biometria')

    def save(self, *args, **kwargs):
        self.indice_de_masa_corporal = (self.peso_en_KG/(self.talla_en_CM**2))  # Calculating IMC
        super(Biometria, self).save(*args, **kwargs)


class ExamFisicoAspectoGeneral(models.Model):
    """ Check if is anormal a pacient default (normal) """
    apariencia_general = models.BooleanField(default=False, null=False, blank=True)
    estado_de_nutricion = models.BooleanField(default=False, null=False, blank=True)
    color_y_textura = models.BooleanField(default=False, null=False, blank=True)
    aspecto = models.BooleanField(default=False, null=False, blank=True)
    lesiones_de_piel = models.BooleanField(default=False, null=False, blank=True)
    tolerancia_irritantes = models.BooleanField(default=False, null=False, blank=True)
    unias = models.BooleanField(verbose_name='uñas', default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_aspecto_general')


# Organo de los sentidos
class ExamFisicoOjos(models.Model):
    """ Check if is anormal a pacient default (normal) """
    pupilas_conjuntivas_corneas = models.BooleanField(default=False, null=False, blank=True)
    vision_profundidad = models.BooleanField(default=False, null=False, blank=True)
    vision_cronomatica = models.BooleanField(default=False, null=False, blank=True)
    vision_periferica = models.BooleanField(default=False, null=False, blank=True)
    forias = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_ojos')


class ExamFisicoOidos(models.Model):
    """ Check if is anormal a pacient default (normal) """
    pabellones = models.BooleanField(default=False, null=False, blank=True)
    otoscopia = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_oidos')


class ExamFisicoNariz(models.Model):
    """ Check if is anormal a pacient default (normal) """
    tabique_cornetes = models.BooleanField(default=False, null=False, blank=True)
    senos_paranasales = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_nariz')


class ExamFisicoBoca(models.Model):
    """ Check if is anormal a pacient default (normal) """
    faringe = models.BooleanField(default=False, null=False, blank=True)
    amigdalas = models.BooleanField(default=False, null=False, blank=True)
    dentadura = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_boca')


# Otros sistemas
class ExamFisicoCuello(models.Model):
    """ Check if is anormal a pacient default (normal) """
    movimientos = models.BooleanField(default=False, null=False, blank=True)
    palpacion = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_cuello')


class ExamFisicoToraxPulmones(models.Model):
    """ Check if is anormal a pacient default (normal) """
    inspeccion = models.BooleanField(default=False, null=False, blank=True)
    palpacion = models.BooleanField(default=False, null=False, blank=True)
    auscultacion = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_torax_pulmones')


class ExamFisicoCorazon(models.Model):
    """ Check if is anormal a pacient default (normal) """
    ritmo = models.BooleanField(default=False, null=False, blank=True)
    ruidos_cardiacos = models.BooleanField(default=False, null=False, blank=True)
    circularion_periferica = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_corazon')


class ExamFisicoAbdomen(models.Model):
    """ Check if is anormal a pacient default (normal) """
    inspeccion = models.BooleanField(default=False, null=False, blank=True)
    papacion_organos = models.BooleanField(default=False, null=False, blank=True)
    anillos_inguinales = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_abdomen')


class ExamFisicoGenitoUnitario(models.Model):
    """ Only show when patient is a women """
    riniones = models.BooleanField(verbose_name='riñones', default=False, null=False, blank=True)
    genitales_externos = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_genito_unitario')


class ExamFisicoColumna(models.Model):
    curvaturas = models.BooleanField(default=False, null=False, blank=True)
    movilidad = models.BooleanField(default=False, null=False, blank=True)
    tono_musculos_paravertebrales = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_columna')


class ExamFisicoExtremidades(models.Model):
    movilidad_miembros_superioes = models.BooleanField(default=False, null=False, blank=True)
    movilidad_miembros_inferiore = models.BooleanField(default=False, null=False, blank=True)
    musculos = models.BooleanField(default=False, null=False, blank=True)
    movilidad_dedos_manos = models.BooleanField(default=False, null=False, blank=True)
    articulaciones = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_extremidades')


class ExamFisicoNeurologico(models.Model):
    esfera_mental = models.BooleanField(default=False, null=False, blank=True)
    sensibilidad_superficial = models.BooleanField(default=False, null=False, blank=True)
    sensibilidad_profunda = models.BooleanField(default=False, null=False, blank=True)
    reflejos = models.BooleanField(default=False, null=False, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='examen_fisico_neurologico')


OPCION = (('normal', 'Normal'),
          ('aumentada', 'Aumentada'),
          ('disminuida', 'Disminuida'))


class ColumnaCervical(models.Model):
    curvatura = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    lordosis_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    cifosis_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    escoliosis_derecha_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    escoliosis_izquierda_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)

    observaciones = models.TextField(null=True, blank=True)

    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='columna_cervical')


class ColumnaDorsal(models.Model):
    curvatura = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    lordosis_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    cifosis_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    escoliosis_derecha_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    escoliosis_izquierda_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)

    observaciones = models.TextField(null=True, blank=True)

    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='columna_dorsal')


class ColumnaLumbar(models.Model):
    curvatura = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    lordosis_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    cifosis_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    escoliosis_derecha_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)
    escoliosis_izquierda_normal = models.CharField(max_length=15, choices=OPCION, default='normal', null=False, blank=False)

    observaciones = models.TextField(null=True, blank=True)

    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='columna_lumbar')


class ConclusionIngreso(models.Model):
    """ Conclusion form to examination of type 'ingreso' """
    ESTADOS = (('apto sin recomendaciones', 'Apto Sin Recomendaciones'),
               ('apto con recomendaciones', 'Apto Con Recomendaciones'),
               ('no apto', 'No Apto'),
               ('aplazado', 'Aplazado'),)
    estado = models.CharField(max_length=30, choices=ESTADOS, null=False, blank=False)
    limitaciones = models.TextField(null=True, blank=True)
    recomendaciones = models.TextField(null=False, blank=False)

    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='conclusiones_ingreso')


class ConclusionRetiro(models.Model):
    """ Conclusion model to examination of type 'retiro' """
    se_encuentran_alteraciones = models.BooleanField(default=False, null=False, blank=True)
    recomendaciones = models.TextField(null=True, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='conclusiones_retiro')


class ConclusionPeriodico(models.Model):
    """ Conclusion model to examination of type 'periodico' """
    resultado_normal = models.BooleanField(default=True, null=False, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='conclusiones_periodico')


class ConclusionPostIncapacidad(models.Model):
    """ Conclusion model to examination of type 'Post-Incapacidad' """
    recomendaciones = models.TextField(null=False, blank=True)
    ocupacional_id = models.OneToOneField(Occupational, null=False, blank=False, on_delete=models.CASCADE,
                                          related_name='conclusiones_post_incapacidad')


