from django import forms

from docapp.models import (Visiometry,
                           Sintomas,
                           AntEnfermedad,
                           AntUsoLentes,
                           AntExamenExterno,
                           Agudeza,
                           Cronomatica)


class VisioForm(forms.ModelForm):
    class Meta:
        model = Visiometry
        exclude = ('ultima_vez_modificaco', 'tipo_examen',)

    def save(self, commit=True):
        instance = super(VisioForm, self).save(commit=False)
        instance.tipo_examen = self.exam_type
        if commit:
            instance.save()
        return instance


sintomas_section = forms.inlineformset_factory(parent_model=Visiometry, model=Sintomas, extra=1, max_num=1,
                                               can_delete=False, fields='__all__')

ant_enfermedad_section = forms.inlineformset_factory(parent_model=Visiometry, model=AntEnfermedad, extra=1, max_num=1,
                                                     can_delete=False, fields='__all__')

ant_uso_lentes_section = forms.inlineformset_factory(parent_model=Visiometry, model=AntUsoLentes, extra=1, max_num=1,
                                                     can_delete=False, fields='__all__')

ant_extra_exams = forms.inlineformset_factory(parent_model=Visiometry, model=AntExamenExterno, extra=1, max_num=1,
                                              can_delete=False, fields='__all__')

agudeza_section = forms.inlineformset_factory(parent_model=Visiometry, model=Agudeza, extra=1, max_num=1,
                                              can_delete=False, fields='__all__')

cronomatica_section = forms.inlineformset_factory(parent_model=Visiometry, model=Cronomatica, extra=1, max_num=1,
                                                  can_delete=False, fields='__all__')
