from django import forms

from docapp.models import Laboratory, ExamenSangre, Examenes


class LabForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        exclude = ('ultima_vez_modificado', 'tipo_examen', 'registrado_por',)

    def save(self, commit=True):
        instance = super(LabForm, self).save(commit=False)
        instance.tipo_examen = self.exam_type
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance


blood_section = forms.inlineformset_factory(parent_model=Laboratory, model=ExamenSangre, extra=1, max_num=1,
                                            can_delete=False, fields='__all__')

exams_section = forms.inlineformset_factory(parent_model=Laboratory, model=Examenes, can_delete=True, fields='__all__')
