from django import forms

from docapp.models import Audiology, Ananmesis, Ant_familiares, Ant_otros, Exposiciones, EstadoActual


class AudioForm(forms.ModelForm):
    class Meta:
        model = Audiology
        exclude = ('last_modify', 'exam_type', 'create_by',)

    def save(self, commit=True):
        instance = super(AudioForm, self).save(commit=False)
        instance.exam_type = self.exam_type
        instance.create_by = self.create_by
        if commit:
            instance.save()
        return instance


class AnaForm(forms.ModelForm):
    class Meta:
        model = Ananmesis
        fields = '__all__'


ananmesis_section = forms.inlineformset_factory(parent_model=Audiology, model=Ananmesis, form=AnaForm, extra=1,
                                                max_num=1, can_delete=False)


class AntFamForm(forms.ModelForm):
    class Meta:
        model = Ant_familiares
        fields = '__all__'


ant_familiar_section = forms.inlineformset_factory(parent_model=Audiology, model=Ant_familiares, form=AntFamForm,
                                                   extra=1, max_num=1, can_delete=False)


class AntOtroForm(forms.ModelForm):
    class Meta:
        model = Ant_otros
        fields = '__all__'


ant_otro_section = forms.inlineformset_factory(parent_model=Audiology, model=Ant_otros, form=AntOtroForm, extra=1,
                                               max_num=1, can_delete=False)


class ExpoForm(forms.ModelForm):
    class Meta:
        model = Exposiciones
        fields = '__all__'


exposicion_section = forms.inlineformset_factory(parent_model=Audiology, model=Exposiciones, form=ExpoForm, extra=1,
                                                 max_num=1, can_delete=False)


class EstActualForm(forms.ModelForm):
    class Meta:
        model = EstadoActual
        fields = '__all__'


estado_actual_section = forms.inlineformset_factory(parent_model=Audiology, model=EstadoActual, form=EstActualForm,
                                                    extra=1, max_num=1, can_delete=False)
