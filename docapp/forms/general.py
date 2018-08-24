from django import forms

from docapp.models import (Empresa, PacienteEmpresa, AntecedentesLaborales, Riesgos, Accidentes, Examinacion,
                           PacienteParticular, Consulta, SimpleExam)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ('nombre', 'nit', 'direccion', 'telefono', 'celular', 'correo_contacto',)
        exclude = ('registrado_por',)

    def save(self, commit=True):
        instance = super(CompanyForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance


""" Formularios para procesos con empresas """


class PacienteEmpresaForm(forms.ModelForm):
    class Meta:
        model = PacienteEmpresa
        fields = ('nombres', 'apellidos', 'identificacion', 'lugar_de_nacimiento', 'fecha_de_nacimiento',
                  'sexo', 'estado_civil', 'numero_de_hijos', 'direccion', 'telefono',
                  'celular', 'ocupacion', 'posicion', 'estrato', 'estudiante_en_entrenamiento',
                  'aprendiz_sena', 'numero_patronal',)
        exclude = ('registrado_por', 'empresa',)

    def save(self, commit=True):
        instance = super(PacienteEmpresaForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        instance.empresa = self.company
        if commit:
            instance.save()
        return instance


class ExaminacionForm(forms.ModelForm):
    class Meta:
        model = Examinacion
        fields = ('tipo', 'estado',)
        exclude = ('registrado_por', 'paciente',)

    def clean(self):
        """ Validate when register exam it's state been pendiente """
        if any(self.errors):
            return

        if hasattr(self, 'initial') and self.cleaned_data.get('estado') != 'pendiente':
            raise forms.ValidationError(
                message='El estado no puede ser diferente a pendiente, apenas se inicia el proceso',
                code='invalid'
            )
        else:
            delattr(self, 'initial')  # Clean form data

    def save(self, commit=True, **kwargs):
        instance = super(ExaminacionForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        instance.paciente = self.person
        if commit:
            instance.save()
        return instance


class AntLaboralesForm(forms.ModelForm):
    class Meta:
        model = AntecedentesLaborales
        fields = ('nombre_empresa', 'ocupacion', 'tiempo', 'uso_epp',)
        exclude = ('registrado_por', 'persona',)

    def save(self, commit=True):
        instance = super(AntLaboralesForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        instance.persona = self.person
        if commit:
            instance.save()
        return instance


class AntLabRiesgosForm(forms.ModelForm):
    class Meta:
        model = Riesgos
        fields = ('fisico', 'fisico', 'quimico',
                  'mecanico', 'ergonomico', 'electrico',
                  'electrico', 'psicologico', 'locativo')
        exclude = ('empresa',)


hazards_inlineformset = forms.inlineformset_factory(parent_model=AntecedentesLaborales, model=Riesgos,
                                                    form=AntLabRiesgosForm, can_delete=False, extra=1, max_num=1)


class AccidenteForm(forms.ModelForm):
    class Meta:
        model = Accidentes
        fields = '__all__'
        exclude = ('empresa',)


accident_inlineformset = forms.inlineformset_factory(parent_model=AntecedentesLaborales, model=Accidentes,
                                                     form=AccidenteForm, can_delete=True)

""" Formularios para procesos con consultas particulares """


class ParticularForm(forms.ModelForm):
    class Meta:
        model = PacienteParticular
        fields = ('nombres', 'apellidos', 'identificacion', 'lugar_de_nacimiento', 'fecha_de_nacimiento',
                  'sexo', 'estado_civil', 'numero_de_hijos', 'direccion', 'telefono',
                  'celular', 'ocupacion', 'estrato', )
        exclude = ('registrado_por',)

    def save(self, commit=True):
        instance = super(ParticularForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance


# TODO Cuando una recepcionista genere una consulta se creará la instancia, simplemente.
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ('razon',)
        exclude = ('registrado_por',)

    def save(self, commit=True):
        instance = super(ConsultaForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance


class RegisterSingleExamForm(forms.ModelForm):
    class Meta:
        model = SimpleExam
        fields = ('nombre',)
        exclude = ('registrado_por', 'resultados',)

    def save(self, commit=True):
        instance = super(RegisterSingleExamForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance


reception_exam_formset = forms.modelformset_factory(model=SimpleExam, can_delete=True, form=RegisterSingleExamForm)


class UpdateSimpleExamForm(forms.ModelForm):
    class Meta:
        model = SimpleExam
        fields = ('nombre', 'resultados', )
        exclude = ('registrado_por', )

    def clean_nombre(self):
        return self.initial['nombre']

    def save(self, commit=True):
        instance = super(UpdateSimpleExamForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance
