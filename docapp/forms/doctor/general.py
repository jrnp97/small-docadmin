from django import forms

from docapp.models import Consulta, SimpleExam


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


class UpdateSimpleExamForm(forms.ModelForm):
    class Meta:
        model = SimpleExam
        fields = '__all__'
        exclude = ('registrado_por', 'nombre', )

    def save(self, commit=True):
        instance = super(UpdateSimpleExamForm, self).save(commit=False)
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance
