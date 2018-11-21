""" Forms manage by receptionists """
from django import forms

from docapp.models import (Empresa, PacienteEmpresa, PacienteParticular, Examinacion, SimpleExam, AntecedentesLaborales,
                           Riesgos, Accidentes)
from labapp.models import LabExam, Laboratorio


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
    laboratorio_id = forms.ModelMultipleChoiceField(queryset=Laboratorio.objects.all())

    class Meta:
        model = Examinacion
        fields = ('tipo', 'laboratorio_id', 'do_exam_altura', 'do_exam_audiologia', 'do_exam_visiometria',)
        exclude = ('registrado_por', 'paciente_id', 'estado', 'manejador_por')
        labels = {
            'tipo': 'Tipo de Examinación',
            'laboratorio_id': 'Seleccione Laboratorio',
            'do_exam_altura': 'Examen de Altura',
            'do_exam_audiologia': 'Examen de Audiologia',
            'do_exam_visiometria': 'Examen de Visiometria'
        }

    def save(self, commit=True):
        instance = super(ExaminacionCreateForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        instance.paciente_id = self.person
        if commit:
            instance.save()
        return instance


simple_exam_inlineformset = forms.inlineformset_factory(parent_model=Examinacion, model=SimpleExam, extra=1,
                                                        can_delete=True, fields='__all__',
                                                        exclude=('registrado_por', 'resultados'))

lab_exam_inlineformset = forms.inlineformset_factory(parent_model=Examinacion, model=LabExam, can_delete=True,
                                                     fields='__all__', extra=1,
                                                     exclude=('registrado_por', 'manejado_por', 'laboratorio_id', ))


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

accident_inlineformset = forms.inlineformset_factory(parent_model=AntecedentesLaborales, model=Accidentes, extra=1,
                                                     can_delete=True, fields='__all__', exclude=('registrado_por',))
