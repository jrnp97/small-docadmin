from django import forms

from docapp.models import Empresa, Paciente, TipoExamen, AntecedentesLaborales, Riesgos


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


class PersonForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ('nombres', 'apellidos', 'identificacion', 'lugar_de_nacimiento', 'fecha_de_nacimiento',
                  'sexo', 'estado_civil', 'numero_de_hijos', 'direccion', 'telefono',
                  'celular', 'ocupacion', 'posicion', 'estrato', 'estudiante_en_entrenamiento',
                  'aprendiz_sena', 'numero_patronal',)
        exclude = ('registrado_por', 'empresa',)

    def save(self, commit=True):
        instance = super(PersonForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        instance.empresa = self.company
        if commit:
            instance.save()
        return instance


class ExamForm(forms.ModelForm):
    class Meta:
        model = TipoExamen
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
        instance = super(ExamForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        instance.paciente = self.person
        if commit:
            instance.save()
        return instance


class AntecedentForm(forms.ModelForm):
    class Meta:
        model = AntecedentesLaborales
        fields = ('nombre_empresa', 'ocupacion', 'tiempo', 'uso_epp',)
        exclude = ('registrado_por', 'persona',)

    def save(self, commit=True):
        instance = super(AntecedentForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        instance.persona = self.person
        if commit:
            instance.save()
        return instance


class AntHazardForm(forms.ModelForm):
    class Meta:
        model = Riesgos
        fields = ('fisico', 'fisico', 'quimico',
                  'mecanico', 'ergonomico', 'electrico',
                  'electrico', 'psicologico', 'locativo')
        exclude = ('empresa',)


hazards_inlineformset = forms.inlineformset_factory(parent_model=AntecedentesLaborales, model=Riesgos,
                                                    form=AntHazardForm, can_delete=False, extra=1, max_num=1)
