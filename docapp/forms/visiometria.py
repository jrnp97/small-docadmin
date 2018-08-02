from django import forms

from docapp.models import (Visiometry,
                           Sintomas,
                           Ant_enfermedad,
                           Ant_uso_lentes,
                           Ant_exam_externo,
                           Agudeza,
                           Cronomatica)


class VisioForm(forms.ModelForm):
    class Meta:
        model = Visiometry
        exclude = ('last_modify', 'exam_type', 'create_by',)

    def save(self, commit=True):
        instance = super(VisioForm, self).save(commit=False)
        instance.exam_type = self.exam_type
        instance.create_by = self.create_by
        if commit:
            instance.save()
        return instance


class SintoForm(forms.ModelForm):
    class Meta:
        model = Sintomas
        fields = '__all__'


sintomas_section = forms.inlineformset_factory(parent_model=Visiometry, model=Sintomas, form=SintoForm,
                                               extra=1, max_num=1, can_delete=False)


class EnfermedadForm(forms.ModelForm):
    class Meta:
        model = Ant_enfermedad
        fields = '__all__'


ant_enfermedad_section = forms.inlineformset_factory(parent_model=Visiometry, model=Ant_enfermedad, form=EnfermedadForm,
                                                     extra=1, max_num=1, can_delete=False)


class UsoLentesForm(forms.ModelForm):
    class Meta:
        model = Ant_uso_lentes
        fields = '__all__'


ant_uso_lentes_section = forms.inlineformset_factory(parent_model=Visiometry, model=Ant_uso_lentes, form=UsoLentesForm,
                                                     extra=1, max_num=1, can_delete=False)


class ExamExtForm(forms.ModelForm):
    class Meta:
        model = Ant_exam_externo
        fields = '__all__'


ant_extra_exams = forms.inlineformset_factory(parent_model=Visiometry, model=Ant_exam_externo, form=ExamExtForm,
                                              extra=1, max_num=1, can_delete=False)


class AgudezaForm(forms.ModelForm):
    class Meta:
        model = Agudeza
        fields = '__all__'


agudeza_section = forms.inlineformset_factory(parent_model=Visiometry, model=Agudeza, form=AgudezaForm, extra=1,
                                              max_num=1, can_delete=False)


class CronoForm(forms.ModelForm):
    class Meta:
        model = Cronomatica
        fields = '__all__'


cronomatica_section = forms.inlineformset_factory(parent_model=Visiometry, model=Cronomatica, form=CronoForm, extra=1,
                                                  max_num=1, can_delete=False)
