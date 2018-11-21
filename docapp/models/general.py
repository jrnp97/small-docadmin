from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import ReceptionProfile, DoctorProfile
from docapp.choices import ExamStates, ExamTipes, CivilState, Sex, ESTRATOS

User = get_user_model()


# class Eps(models.Model):
#     eps = models.CharField(max_length=50, null=False, blank=False)
#
#     def __str__(self):
#         return self.eps
#
#
# class Afp(models.Model):
#     afp = models.CharField(max_length=50, null=False, blank=False)
#
#     def __str__(self):
#         return self.afp
#
#
# class Arl(models.Model):
#     arl = models.CharField(max_length=50, null=False, blank=False)
#
#     def __str__(self):
#         return self.arl


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
    nombres = models.CharField(max_length=300, null=False, blank=False)
    apellidos = models.CharField(max_length=300, null=False, blank=False)
    identificacion = models.PositiveIntegerField(unique=True)
    lugar_de_nacimiento = models.CharField(max_length=500, null=False, blank=False)
    fecha_de_nacimiento = models.DateField(null=False, blank=False)
    # eps = models.ForeignKey(Eps, on_delete=models.CASCADE, null=True)
    # arl = models.ForeignKey(Arl, on_delete=models.CASCADE, null=True)
    # fondo_pensiones = models.ForeignKey(Afp, on_delete=models.CASCADE, null=True)
    eps = models.CharField(max_length=100)
    arl = models.CharField(max_length=100)
    fondo_pensiones = models.CharField(max_length=100, null=True, blank=True)
    sexo = models.CharField(max_length=15, choices=Sex.ALL, null=False, blank=False)
    estado_civil = models.CharField(max_length=20, choices=CivilState.ALL, null=False, blank=False)
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
    tipo = models.CharField(max_length=20, choices=ExamTipes.ALL, null=False, blank=False)
    estado = models.CharField(max_length=20, choices=ExamStates.ALL, default=ExamStates.PENDIENTE)
    doctor_estado = models.CharField(max_length=20, choices=ExamStates.PROCESS, default=ExamStates.NO_ASIG)
    lab_estado = models.CharField(max_length=20, choices=ExamStates.PROCESS, default=ExamStates.NO_ASIG)

    do_exam_altura = models.BooleanField(default=False, null=False, blank=True)
    do_exam_audiologia = models.BooleanField(default=False, null=False, blank=True)
    do_exam_visiometria = models.BooleanField(default=False, null=False, blank=True)

    # laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, related_name='examinaciones')
    paciente_id = models.ForeignKey(PacienteEmpresa, on_delete=models.CASCADE, related_name='examinaciones')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE, related_name='examinaciones')
    manejador_por = models.ForeignKey(DoctorProfile, null=True, blank=True, on_delete=models.CASCADE,
                                      related_name='examinaciones')

    def __str__(self):
        return self.tipo

    def get_doctor_process(self):
        normal_exams = [hasattr(self, 'ocupacional')]
        if self.do_exam_altura:
            normal_exams.append(hasattr(self, 'altura'))
        if self.do_exam_audiologia:
            normal_exams.append(hasattr(self, 'audiologia'))
        if self.do_exam_visiometria:
            normal_exams.append(hasattr(self, 'visiometria'))

        inter_exams = []
        for inter in self.examenes_internos.all():
            if inter.resultados != '':
                inter_exams.append(True)

        percentage = float(100) / (len(self.examenes_internos.all()) + len(normal_exams))

        return float("{:.2f}".format((len(inter_exams) + normal_exams.count(True)) * percentage))

    def get_lab_process(self):
        exams = self.examenes_laboratorios.all()
        if exams:
            lab_exams = []
            for exam in exams:
                if exam.resultados.all():
                    lab_exams.append(True)

            percentage = float(100) / len(exams)

            return float("{:.2f}".format(len(lab_exams) * percentage))
        else:
            return 0.0

    def update_doctor(self):
        if self.doctor_estado == ExamStates.ASIGNADO:
            self.doctor_estado = ExamStates.INICIADO
            self.save()

    def update_lab(self):
        change = False
        if self.lab_estado == ExamStates.ASIGNADO:
            self.lab_estado = ExamStates.INICIADO
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        response = super(SimpleExam, self).save(force_insert, force_update, using, update_fields)
        self.examinacion_id.update_doctor()
        return response


# Models to manage simple person information
class PacienteParticular(models.Model):
    """ Model to save simple person information """
    nombres = models.CharField(max_length=300, null=False, blank=False)
    apellidos = models.CharField(max_length=300, null=False, blank=False)
    identificacion = models.PositiveIntegerField(unique=True)
    lugar_de_nacimiento = models.CharField(max_length=500, null=False, blank=False)
    fecha_de_nacimiento = models.DateField(null=False, blank=False)
    eps = models.CharField(verbose_name='EPS', max_length=50, null=False, blank=False)
    arl = models.CharField(verbose_name='ARL', max_length=50, null=False, blank=False)
    fondo_pensiones = models.CharField(max_length=50, null=False, blank=False)
    sexo = models.CharField(max_length=15, choices=Sex.ALL, null=False, blank=False)
    direccion = models.CharField(max_length=500, null=False, blank=False)
    telefono = models.PositiveIntegerField(default=0)
    celular = models.PositiveIntegerField(null=False, blank=False)
    ocupacion = models.CharField(max_length=500, null=False, blank=False)
    estrato = models.PositiveIntegerField(null=False)
    nombre_del_responsable = models.CharField(max_length=50, null=True, blank=True)
    estado_civil = models.CharField(max_length=20, choices=CivilState.ALL, null=False, blank=False)
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
    estado = models.CharField(max_length=20, choices=ExamStates.ALL, default=ExamStates.PENDIENTE)
    razon = models.TextField(default='', null=False, blank=False)
    paciente_id = models.ForeignKey(PacienteParticular, null=False, blank=True, on_delete=models.CASCADE,
                                    related_name='consultas')
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='consultas')
