""" Forms manage by receptionists """
from django import forms

from docapp.models import (Empresa, PacienteEmpresa, PacienteParticular, Examinacion, SimpleExam, AntecedentesLaborales,
                           Riesgos, Accidentes)
from labapp.models import LabExam


# Company Forms
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'
        exclude = ('registrado_por',)

    def save(self, commit=True):
        instance = super(CompanyForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance


# Employ Forms
class PacienteEmpresaForm(forms.ModelForm):
    class Meta:
        model = PacienteEmpresa
        fields = '__all__'
        exclude = ('registrado_por', 'empresa',)

    def save(self, commit=True):
        instance = super(PacienteEmpresaForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        instance.empresa = self.company
        if commit:
            instance.save()
        return instance


# Particular Forms
class PacienteParticularForm(forms.ModelForm):
    class Meta:
        model = PacienteParticular
        fields = '__all__'
        exclude = ('registrado_por',)

    def save(self, commit=True):
        instance = super(PacienteParticularForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance


# Examination Forms
class ExaminacionCreateForm(forms.ModelForm):
    altura = forms.BooleanField(label='Examen de Altura')  # Select if altura exam will do
    audiologia = forms.BooleanField(label='Examen de Audiologia')  # Select if audiologia exam will do
    visiometria = forms.BooleanField(label='Examen de Visiometria')  # Select if audiology exam will do

    class Meta:
        model = Examinacion
        fields = '__all__'
        exclude = ('registrado_por', 'paciente_id', 'estado', 'manejador_por')
        labels = {
            'tipo': 'Tipo de Examinación',
            'laboratorio_id': 'Seleccione Laboratorio',
        }

    def save(self, commit=True, **kwargs):
        instance = super(ExaminacionCreateForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        instance.paciente = self.person
        if commit:
            instance.save()
        return instance


simple_exam_inlineformset = forms.inlineformset_factory(parent_model=Examinacion, model=SimpleExam, can_delete=True,
                                                        fields='__all__', exclude=('registrado_por', 'resultados'))

lab_exam_inlineformset = forms.modelformset_factory(model=LabExam, can_delete=True, fields='__all__',
                                                    exclude=('registrado_por', 'manejado_por', 'laboratorio_id  '))


# Appointment Forms (Receptionist only send a request and a register must be create)
# Antecedent Forms
class AntLaboralesForm(forms.ModelForm):
    class Meta:
        model = AntecedentesLaborales
        fields = '__all__'
        exclude = ('registrado_por', 'persona',)

    def save(self, commit=True):
        instance = super(AntLaboralesForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        instance.persona = self.person
        if commit:
            instance.save()
        return instance


hazards_inlineformset = forms.inlineformset_factory(parent_model=AntecedentesLaborales, model=Riesgos, extra=1,
                                                    max_num=1, can_delete=False, fields='__all__')

accident_inlineformset = forms.inlineformset_factory(parent_model=AntecedentesLaborales, model=Accidentes,
                                                     can_delete=True, fields='__all__')
