from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import ReceptionProfile

User = get_user_model()


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    nit = models.PositiveIntegerField(verbose_name='NIT')
    direction = models.CharField(max_length=500, null=False, blank=False)
    land_line = models.PositiveIntegerField(null=True)
    cellphone = models.PositiveIntegerField(null=False, blank=False)
    contact = models.EmailField(null=False, blank=False)

    last_modify = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    create_by = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    last_name = models.CharField(max_length=300, null=False, blank=False)
    identification = models.PositiveIntegerField(unique=True)
    born_place = models.CharField(max_length=500, null=False, blank=False)
    born_date = models.DateField(null=False, blank=False)

    SEXS = (
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino')
    )
    sex = models.CharField(max_length=15, choices=SEXS, null=False, blank=False)

    CIVIL_STATES = (
        ('soltero', 'Soltero'),
        ('casado', 'Casado'),
        ('viudo', 'Viudo'),
        ('union libre', 'Union Libre')
    )

    civil_state = models.CharField(max_length=20, choices=CIVIL_STATES, null=False, blank=False)
    number_sons = models.PositiveIntegerField()
    direction = models.CharField(max_length=500, null=False, blank=False)
    land_line = models.PositiveIntegerField(null=True)
    cellphone = models.PositiveIntegerField(null=False, blank=False)
    occupation = models.CharField(max_length=500, null=False, blank=False)
    position = models.CharField(max_length=500, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False)
    stratus = models.PositiveIntegerField()
    # scholarship = ""
    training_student = models.BooleanField(default=False)
    sena_learner = models.BooleanField(default=False)
    number_patronal = models.PositiveIntegerField(null=False, blank=False)

    last_modify = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    create_by = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.name} {self.last_name}"

    def get_antecedents(self):
        antecedents = self.antecedents.all()
        if len(antecedents) > 0:
            return antecedents
        else:
            return None

    def get_exams(self):
        exams = self.exams.all()
        if len(exams) > 0:
            return exams
        else:
            return None


class ExamType(models.Model):
    TYPES = (
        ('ingreso', 'Ingreso'),
        ('periodico', 'Periodico'),
        ('retiro', 'Retiro'),
        ('reubicacion', 'Re-Ubicacion'),
        ('post-incapacidad', 'Post-Incapacidad')
    )

    name = models.CharField(max_length=20, choices=TYPES, null=False, blank=False)
    person = models.ForeignKey(Person, null=False, blank=False, on_delete=models.CASCADE, related_name='exams')
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    STATES = (
        ('pendiente', 'Pendiente'),
        ('iniciado', 'Iniciado'),
        ('problemas', 'Problema'),
        ('finalizado', 'Finalizado'),
    )
    state = models.CharField(max_length=20, choices=STATES, null=False, blank=False)
    create_by = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AntecedentJobs(models.Model):
    company = models.CharField(max_length=300, null=False, blank=False)
    occupation = models.CharField(max_length=500, null=False, blank=False)
    time = models.PositiveIntegerField(null=False, blank=False)
    uso_epp = models.BooleanField(default=False, null=False, blank=False)

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='antecedents')

    last_modify = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=False)
    create_by = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.company


class Hazards(models.Model):
    work = models.OneToOneField(AntecedentJobs,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='hazards')
    fisico = models.BooleanField(default=False, null=False, blank=False)
    quimico = models.BooleanField(default=False, null=False, blank=False)
    mecanico = models.BooleanField(default=False, null=False, blank=False)
    ergonomico = models.BooleanField(default=False, null=False, blank=False)
    electrico = models.BooleanField(default=False, null=False, blank=False)
    psicologico = models.BooleanField(default=False, null=False, blank=False)
    locativo = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return self.get_number_hazard()

    def get_number_hazard(self):
        hazards = (self.fisico,
                   self.quimico,
                   self.mecanico,
                   self.ergonomico,
                   self.electrico,
                   self.psicologico,
                   self.locativo,
                   )
        return str(hazards.count(True))

    def as_dict(self):
        return {
            'fisico': self.fisico,
            'quimico': self.quimico,
            'mecanico': self.mecanico,
            'ergonomico': self.ergonomico,
            'electrico': self.electrico,
            'psicologico': self.psicologico,
            'locativo': self.locativo,
        }


class JobAccidents(models.Model):
    secuelas = models.TextField(null=False, blank=False)
    tipo = models.CharField(max_length=200, null=False, blank=False)
    atendido = models.BooleanField(default=False, null=False, blank=False)
    calificado = models.BooleanField(default=False, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    work = models.ForeignKey(AntecedentJobs, on_delete=models.CASCADE, related_name='accidents')

    create_by = models.ForeignKey(ReceptionProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo

    def as_dict(self):
        return {
            'secuelas': self.secuelas,
            'tipo': self.tipo,
            'atendido': self.atendido,
            'calificado': self.calificado,
            'fecha': self.fecha,
            'description': self.description
        }
