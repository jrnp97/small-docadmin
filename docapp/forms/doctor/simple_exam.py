from django import forms

from docapp.models import SimpleExam


class SimpleExamForm(forms.ModelForm):
    class Meta:
        model = SimpleExam
        exclude = ('ultima_vez_modificado', 'examinacion_id', 'nombre', 'registrado_por')

    def save(self, commit=True):
        instance = super(SimpleExamForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
