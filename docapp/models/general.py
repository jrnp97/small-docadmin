from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import ReceptionProfile

User = get_user_model()


# Create your models here.
class Empresa(models.Model):
    nombre = models.CharField(max_length=300, null=False, blank=False, unique=True)
    nit = models.PositiveIntegerField(verbose_name='NIT')
    direccion = models.CharField(max_length=500, null=False, blank=False)
    telefono = models.PositiveIntegerField(null=True)
    celular = models.PositiveIntegerField(null=False, blank=False)
    correo_contacto = models.EmailField(null=False, blank=False)

    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    nombres = models.CharField(max_length=300, null=False, blank=False)
    apellidos = models.CharField(max_length=300, null=False, blank=False)
    identificacion = models.PositiveIntegerField(unique=True)
    lugar_de_nacimiento = models.CharField(max_length=500, null=False, blank=False)
    fecha_de_nacimiento = models.DateField(null=False, blank=False)

    SEXOS = (
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino')
    )
    sexo = models.CharField(max_length=15, choices=SEXOS, null=False, blank=False)

    ESTADOS_CIVILES = (
        ('soltero', 'Soltero'),
        ('casado', 'Casado'),
        ('viudo', 'Viudo'),
        ('union libre', 'Union Libre')
    )

    estado_civil = models.CharField(max_length=20, choices=ESTADOS_CIVILES, null=False, blank=False)
    numero_de_hijos = models.PositiveIntegerField()
    direccion = models.CharField(max_length=500, null=False, blank=False)
    telefono = models.PositiveIntegerField(null=True)
    celular = models.PositiveIntegerField(null=False, blank=False)
    ocupacion = models.CharField(max_length=500, null=False, blank=False)
    posicion = models.CharField(max_length=500, null=False, blank=False)
    estrato = models.PositiveIntegerField()
    estudiante_en_entrenamiento = models.BooleanField(default=False)
    aprendiz_sena = models.BooleanField(default=False)
    numero_patronal = models.PositiveIntegerField(null=False, blank=False)

    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, related_name='empleados')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.nombres} {self.apellidos}"

    def get_antecedents(self):
        antecedents = self.antecedentes.all()
        if len(antecedents) > 0:
            return antecedents
        else:
            return None

    def get_exams(self):
        exams = self.examenes.all()
        if len(exams) > 0:
            return exams
        else:
            return None


class TipoExamen(models.Model):
    TIPOS = (
        ('ingreso', 'Ingreso'),
        ('periodico', 'Periodico'),
        ('retiro', 'Retiro'),
        ('reubicacion', 'Re-Ubicacion'),
        ('post-incapacidad', 'Post-Incapacidad')
    )
    tipo = models.CharField(max_length=20, choices=TIPOS, null=False, blank=False)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('iniciado', 'Iniciado'),
        ('problemas', 'Problema'),
        ('finalizado', 'Finalizado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, null=False, blank=False)
    registrado_por = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='examenes')

    def __str__(self):
        return self.tipo

    def get_process(self):
        examenes_done = [hasattr(self, 'visiometria'), hasattr(self, 'audiologia'),
                         hasattr(self, 'ocupacional'), hasattr(self, 'laboratorio')]
        return examenes_done.count(True) * 25

    def finished(self):
        examenes_done = [hasattr(self, 'visiometria'), hasattr(self, 'audiologia'),
                         hasattr(self, 'ocupacional'), hasattr(self, 'laboratorio')]
        return all(examenes_done)

    def update_state(self):
        process = self.get_process()
        change = False
        if self.estado == 'pendiente' and process > 0 and process < 100:
            self.estado = 'iniciado'
            change = True
        elif self.estado == 'iniciado' and process == 100:
            self.estado = 'finalizado'
            change = True
        if change:
            self.save()


class AntecedentesLaborales(models.Model):
    nombre_empresa = models.CharField(max_length=300, null=False, blank=False)
    ocupacion = models.CharField(max_length=500, null=False, blank=False)
    tiempo = models.PositiveIntegerField(null=False, blank=False)
    uso_epp = models.BooleanField(default=False, null=False, blank=False)

    persona = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='antecedentes')

    ultima_vez_modificado = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    registrado_por = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE, related_name='antecedentes')

    def __str__(self):
        return self.nombre_empresa


class Riesgos(models.Model):
    fisico = models.BooleanField(default=False, null=False, blank=False)
    quimico = models.BooleanField(default=False, null=False, blank=False)
    mecanico = models.BooleanField(default=False, null=False, blank=False)
    ergonomico = models.BooleanField(default=False, null=False, blank=False)
    electrico = models.BooleanField(default=False, null=False, blank=False)
    psicologico = models.BooleanField(default=False, null=False, blank=False)
    locativo = models.BooleanField(default=False, null=False, blank=False)

    empresa = models.OneToOneField(AntecedentesLaborales, on_delete=models.CASCADE, primary_key=True, related_name='hazards')

    def __str__(self):
        return self.get_number_hazard()

    def get_number_hazard(self):
        hazards = (self.fisico, self.quimico, self.mecanico, self.ergonomico,
                   self.electrico, self.psicologico, self.locativo,)
        return str(hazards.count(True))

    def get_label_hazards(self):
        hazards = {'fisico': self.fisico, 'quimico': self.quimico, 'mecanico': self.mecanico,
                   'ergonomico': self.ergonomico, 'electrico': self.electrico, 'psicologico': self.psicologico,
                   'locativo': self.locativo
                   }

        return ", ".join([key for key, val in hazards.items() if val])
