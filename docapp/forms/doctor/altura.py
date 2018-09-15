from django import forms

from docapp.models import Altura, Questions


class AlturaForm(forms.ModelForm):
    class Meta:
        model = Altura
        exclude = ('ultima_vez_modificaco', 'examinacion_id',)

    def save(self, commit=True):
        instance = super(AlturaForm, self).save(commit=False)
        instance.examinacion_id = self.exam_type
        if commit:
            instance.save()
        return instance


question_section = forms.inlineformset_factory(parent_model=Altura, model=Questions, extra=1, max_num=1,
                                               can_delete=False, fields='__all__')
