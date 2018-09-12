from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import ReceptionProfile, DoctorProfile
from labapp.models import Laboratorio

User = get_user_model()


class Eps(models.Model):
    eps = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.eps


class Afp(models.Model):
    afp = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.afp


class Arl(models.Model):
    arl = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.arl


# Models to manage company employs
class Empresa(models.Model):
    """ Model to save company information """
    nombre = models.CharField(max_length=300, null=False, blank=False, unique=True)
    nit = models.PositiveIntegerField(verbose_name='NIT')
    direccion = models.CharField(max_length=500, null=False, blank=False)
    telefono = models.PositiveIntegerField(default=0)
    celular = models.PositiveIntegerField(null=False, blank=False)
    correo_contacto = models.EmailField(null=False, blank=False)

    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE, related_name='empresas')

    def __str__(self):
        return self.nombre


class PacienteEmpresa(models.Model):
    """ Model to save company employ information """
    SEXOS = (
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino')
    )

    ESTADOS_CIVILES = (
        ('soltero', 'Soltero'),
        ('casado', 'Casado'),
        ('viudo', 'Viudo'),
        ('union libre', 'Union Libre')
    )

    ESTRATOS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    nombres = models.CharField(max_length=300, null=False, blank=False)
    apellidos = models.CharField(max_length=300, null=False, blank=False)
    identificacion = models.PositiveIntegerField(unique=True)
    lugar_de_nacimiento = models.CharField(max_length=500, null=False, blank=False)
    fecha_de_nacimiento = models.DateField(null=False, blank=False)
    eps = models.ForeignKey(Eps, on_delete=models.CASCADE, null=True)
    arl = models.ForeignKey(Arl, on_delete=models.CASCADE, null=True)
    fondo_pensiones = models.ForeignKey(Afp, on_delete=models.CASCADE, null=True)
    sexo = models.CharField(max_length=15, choices=SEXOS, null=False, blank=False)
    estado_civil = models.CharField(max_length=20, choices=ESTADOS_CIVILES, null=False, blank=False)
    numero_de_hijos = models.PositiveIntegerField(default=0)
    direccion = models.CharField(max_length=500, null=False, blank=False)
    telefono = models.PositiveIntegerField(default=0)
    celular = models.PositiveIntegerField(null=False, blank=False)
    ocupacion = models.CharField(max_length=500, null=False, blank=False)
    posicion = models.CharField(max_length=500, null=False, blank=False)
    estrato = models.CharField(max_length=20, choices=ESTRATOS, null=False, blank=False)
    estudiante_en_entrenamiento = models.BooleanField(default=False)
    aprendiz_sena = models.BooleanField(default=False)
    numero_patronal = models.PositiveIntegerField(null=False, blank=False)

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, related_name='empleados')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE, related_name='personal_empresa')
    avatar = models.ImageField(upload_to='avatars/patients_company', null=True, blank=True,
                               default="avatars/default.png")

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    def get_antecedents(self):
        antecedents = self.antecedentes.all()
        if len(antecedents) > 0:
            return antecedents
        else:
            return None

    def get_exams(self):
        exams = self.examinaciones.all()
        if len(exams) > 0:
            return exams
        else:
            return None


class Examinacion(models.Model):
    """ Model to register a process over a employ company """
    TIPOS = (('ingreso', 'Ingreso'),
             ('periodico', 'Periodico'),
             ('retiro', 'Retiro'),
             ('reubicacion', 'Re-Ubicacion'),
             ('post-incapacidad', 'Post-Incapacidad'))
    tipo = models.CharField(max_length=20, choices=TIPOS, null=False, blank=False)

    ESTADOS = (('pendiente', 'Pendiente'),
               ('iniciado', 'Iniciado'),
               ('en problemas', 'En Problema'),
               ('finalizado', 'Finalizado'),)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', null=False, blank=False)

    do_exam_altura = models.BooleanField(default=False, null=False, blank=True)
    do_exam_audiologia = models.BooleanField(default=False, null=False, blank=True)
    do_exam_visiometria = models.BooleanField(default=False, null=False, blank=True)

    laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, related_name='examinaciones')
    paciente_id = models.ForeignKey(PacienteEmpresa, on_delete=models.CASCADE, related_name='examinaciones')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE, related_name='examinaciones')
    manejador_por = models.ForeignKey(DoctorProfile, null=True, blank=True, on_delete=models.CASCADE,
                                      related_name='examinaciones')

    def __str__(self):
        return self.tipo

    def get_process(self):
        # TODO CHANGE
        examenes_done = [hasattr(self, 'visiometria'), hasattr(self, 'audiologia'),
                         hasattr(self, 'ocupacional'), hasattr(self, 'laboratorio')]
        return examenes_done.count(True) * 25

    def finished(self):
        # TODO CHANGE
        examenes_done = [hasattr(self, 'visiometria'), hasattr(self, 'audiologia'),
                         hasattr(self, 'ocupacional'), hasattr(self, 'laboratorio')]
        return all(examenes_done)

    def update_state(self):
        # TODO CHANGE
        process = self.get_process()
        change = False
        if self.estado == 'pendiente' and 0 < process < 100:
            self.estado = 'iniciado'
            change = True
        elif self.estado == 'iniciado' and process == 100:
            self.estado = 'finalizado'
            change = True
        if change:
            self.save()


class AntecedentesLaborales(models.Model):
    """ Model to save Antecedents only can fill a doctor """
    nombre_empresa = models.CharField(max_length=300, null=False, blank=False)
    ocupacion = models.CharField(max_length=500, null=False, blank=False)
    tiempo = models.PositiveIntegerField(null=False, blank=False)
    uso_epp = models.BooleanField(default=False, null=False, blank=False)

    persona = models.ForeignKey(PacienteEmpresa, on_delete=models.CASCADE, related_name='antecedentes')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='antecedentes')

    def __str__(self):
        return self.nombre_empresa


class Riesgos(models.Model):
    """ Model binding with AntecedentesLaborales to define hazards """
    fisico = models.BooleanField(default=False, null=False, blank=False)
    quimico = models.BooleanField(default=False, null=False, blank=False)
    mecanico = models.BooleanField(default=False, null=False, blank=False)
    ergonomico = models.BooleanField(default=False, null=False, blank=False)
    electrico = models.BooleanField(default=False, null=False, blank=False)
    psicologico = models.BooleanField(default=False, null=False, blank=False)
    locativo = models.BooleanField(default=False, null=False, blank=False)

    antecedente_id = models.OneToOneField(AntecedentesLaborales, on_delete=models.CASCADE, related_name='riesgos')

    def __str__(self):
        return self.get_number_hazard()

    def get_number_hazard(self):
        hazards = (self.fisico, self.quimico, self.mecanico, self.ergonomico,
                   self.electrico, self.psicologico, self.locativo,)
        return str(hazards.count(True))

    def get_label_hazards(self):
        data = vars(self)
        data.pop('_state', None)
        data.pop('id')
        data.pop('antecedente_id_id', None)
        data.pop('_antecedente_id_cache', None)
        return ", ".join([key for key, val in vars(self).items() if val])


class Accidentes(models.Model):
    """ Model to register accidentos of a previous work this could be n formsets """
    tipo = models.CharField(max_length=200, null=False, blank=False)
    secuelas = models.TextField(null=False, blank=False)
    atendido = models.BooleanField(default=False, null=False, blank=False)
    calificado = models.BooleanField(default=False, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    descripcion = models.TextField(null=False, blank=False)

    antecedente_id = models.ForeignKey(AntecedentesLaborales, on_delete=models.CASCADE, related_name='accidentes')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)


class SimpleExam(models.Model):
    """ Model to save custom exams manage inside enterprise """
    nombre = models.CharField(max_length=50, null=False, blank=False)
    examinacion_id = models.ForeignKey(Examinacion, on_delete=models.CASCADE, related_name='examenes_internos')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, null=False, blank=False, on_delete=models.PROTECT,
                                       related_name='examenes_internos')

    resultados = models.TextField(default='', null=False, blank=True)


# Models to manage simple person information
class PacienteParticular(models.Model):
    """ Model to save simple person information """
    SEXOS = (
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino')
    )

    ESTADOS_CIVILES = (
        ('soltero', 'Soltero'),
        ('casado', 'Casado'),
        ('viudo', 'Viudo'),
        ('union libre', 'Union Libre')
    )
    nombres = models.CharField(max_length=300, null=False, blank=False)
    apellidos = models.CharField(max_length=300, null=False, blank=False)
    identificacion = models.PositiveIntegerField(unique=True)
    lugar_de_nacimiento = models.CharField(max_length=500, null=False, blank=False)
    fecha_de_nacimiento = models.DateField(null=False, blank=False)
    eps = models.CharField(verbose_name='EPS', max_length=50, null=False, blank=False)
    arl = models.CharField(verbose_name='ARL', max_length=50, null=False, blank=False)
    fondo_pensiones = models.CharField(max_length=50, null=False, blank=False)
    sexo = models.CharField(max_length=15, choices=SEXOS, null=False, blank=False)
    direccion = models.CharField(max_length=500, null=False, blank=False)
    telefono = models.PositiveIntegerField(default=0)
    celular = models.PositiveIntegerField(null=False, blank=False)
    ocupacion = models.CharField(max_length=500, null=False, blank=False)
    estrato = models.PositiveIntegerField(null=False)
    nombre_del_responsable = models.CharField(max_length=50, null=True, blank=True)
    estado_civil = models.CharField(max_length=20, choices=ESTADOS_CIVILES, null=False, blank=False)
    numero_de_hijos = models.PositiveIntegerField(default=0)

    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE, related_name='particulares')
    avatar = models.ImageField(upload_to='avatars/patients_particular', null=True, blank=True,
                               default="avatars/default.png")

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Consulta(models.Model):
    """ Model to save appointment description """
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('iniciado', 'Iniciado'),
        ('finalizado', 'Finalizado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', null=False, blank=False)
    razon = models.TextField(default='', null=False, blank=False)
    paciente_id = models.ForeignKey(PacienteParticular, null=False, blank=True, on_delete=models.CASCADE,
                                    related_name='consultas')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='consultas')
