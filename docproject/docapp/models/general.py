from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    nit = models.PositiveIntegerField(verbose_name='NIT')
    direction = models.CharField(max_length=500, null=False, blank=False)
    land_line = models.PositiveIntegerField(max_length=7, null=True)
    cellphone = models.PositiveIntegerField(max_length=10, null=False, blank=False)
    contact = models.EmailField(null=False, blank=False)

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
    land_line = models.PositiveIntegerField(max_length=7, null=True)
    cellphone = models.PositiveIntegerField(max_length=10, null=False, blank=False)
    occupation = models.CharField(max_length=500, null=False, blank=False)
    position = models.CharField(max_length=500, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False)
    stratus = models.PositiveIntegerField(max_length=1)
    # scholarship = ""
    training_student = models.BooleanField(default=False)
    sena_learner = models.BooleanField(default=False)
    number_patronal = models.PositiveIntegerField(null=False, blank=False)

    create_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name} {self.name}"


class ExamType(models.Model):
    TYPES = (
        ('ingreso', 'Ingreso'),
        ('periodico', 'Periodico'),
        ('retiro', 'Retiro'),
        ('reubicacion', 'Re-Ubicacion'),
        ('post-incapacidad', 'Post-Incapacidad')
    )

    name = models.CharField(max_length=20, null=False, blank=False)

    persons = models.ManyToManyField(Person, through='PersonExamType')

    def __str__(self):
        return self.name


class PersonExamType(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)


class AntecedentJobs(models.Model):
    company = models.CharField(max_length=300, null=False, blank=False)
    occupation = models.CharField(max_length=500, null=False, blank=False)
    time = models.PositiveIntegerField(null=False, blank=False)
    uso_epp = models.BooleanField(default=False, null=False, blank=False)

    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class JobAccidents(models.Model):
    secuelas = models.TextField(null=False, blank=False)
    tipo = models.CharField(max_length=200, null=False, blank=False)
    atentido = models.BooleanField(default=False, null=False, blank=False)
    calificado = models.BooleanField(default=False, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    work = models.ForeignKey(AntecedentJobs, on_delete=models.CASCADE)


class Hazards(models.Model):
    fisico = models.BooleanField(default=False, null=False, blank=False)
    quimico = models.BooleanField(default=False, null=False, blank=False)
    mecanico = models.BooleanField(default=False, null=False, blank=False)
    ergonomico = models.BooleanField(default=False, null=False, blank=False)
    electrico = models.BooleanField(default=False, null=False, blank=False)
    psicologico = models.BooleanField(default=False, null=False, blank=False)
    locativo = models.BooleanField(default=False, null=False, blank=False)

    anecedentes = models.OneToOneField(AntecedentJobs, on_delete=models.CASCADE, parent_link=True)

