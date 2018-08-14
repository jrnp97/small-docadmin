from django import forms

from docapp.models import (Audiology,
                           Ananmesis,
                           AntFamiliares,
                           OtrosAntecedentes,
                           ExposicionAudifonos, ExposicionMotocicleta, ExposicionAutomotriz, ExposicionMaquinariaPesada,
                           RuidoMolestia, VolumenTv, FrasesRepetidas, Escucha, EscuchaRuido,
                           Information,
                           Otoscopia)


class AudioForm(forms.ModelForm):
    class Meta:
        model = Audiology
        exclude = ('ultima_vez_modificado', 'tipo_examen', 'registrado_por',)

    def save(self, commit=True):
        instance = super(AudioForm, self).save(commit=False)
        instance.tipo_examen = self.exam_type
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance


ananmesis_section = forms.inlineformset_factory(parent_model=Audiology, model=Ananmesis, extra=1, max_num=1,
                                                can_delete=False, fields='__all__')

ant_familiar_section = forms.inlineformset_factory(parent_model=Audiology, model=AntFamiliares, extra=1, max_num=1,
                                                   can_delete=False, fields='__all__')

ant_otro_section = forms.inlineformset_factory(parent_model=Audiology, model=OtrosAntecedentes, extra=1, max_num=1,
                                               can_delete=False, fields='__all__')

information_section = forms.inlineformset_factory(parent_model=Audiology, model=Information, extra=1, max_num=1,
                                                  can_delete=False, fields='__all__')

otoscopia_section = forms.inlineformset_factory(parent_model=Audiology, model=Otoscopia, extra=1, max_num=1,
                                                can_delete=False, fields='__all__')


class CleanChilds(object):
    def clean(self):
        return True


# Exposiciones
class ExpoAudifonos(forms.ModelForm):
    class Meta:
        model = ExposicionAudifonos
        fields = '__all__'


exposicion_audifonos_section = forms.inlineformset_factory(parent_model=Audiology, model=ExposicionAudifonos,
                                                           form=ExpoAudifonos, extra=1, max_num=1, can_delete=False,)


class ExpoMotocicleta(forms.ModelForm):
    class Meta:
        model = ExposicionMotocicleta
        fields = '__all__'


exposicion_moto_section = forms.inlineformset_factory(parent_model=Audiology, model=ExposicionMotocicleta,
                                                      form=ExpoMotocicleta, extra=1, max_num=1, can_delete=False, )


class ExpoAutomotriz(forms.ModelForm):
    class Meta:
        model = ExposicionAutomotriz
        fields = '__all__'


exposicion_auto_section = forms.inlineformset_factory(parent_model=Audiology, model=ExposicionAutomotriz,
                                                      form=ExpoAutomotriz, extra=1, max_num=1, can_delete=False, )


class ExpoMaquinariaPesada(forms.ModelForm):
    class Meta:
        model = ExposicionMaquinariaPesada
        fields = '__all__'


exposicion_pesada_section = forms.inlineformset_factory(parent_model=Audiology, model=ExposicionMaquinariaPesada,
                                                        form=ExpoMaquinariaPesada, extra=1, max_num=1,
                                                        can_delete=False, )


# Estado Actual
class EstRuidoMolestia(forms.ModelForm):
    class Meta:
        model = RuidoMolestia
        fields = '__all__'


estado_actual_ruido_molestia_section = forms.inlineformset_factory(parent_model=Audiology, model=RuidoMolestia,
                                                                   form=EstRuidoMolestia,
                                                                   extra=1, max_num=1, can_delete=False, )


class EstVolumenTv(forms.ModelForm):
    class Meta:
        model = VolumenTv
        fields = '__all__'


estado_actual_volumen_tv_section = forms.inlineformset_factory(parent_model=Audiology, model=VolumenTv,
                                                               form=EstVolumenTv, extra=1,
                                                               max_num=1, can_delete=False, )


class EstFrasesRepetidas(forms.ModelForm):
    class Meta:
        model = FrasesRepetidas
        fields = '__all__'


estado_actual_frases_repetidas_section = forms.inlineformset_factory(parent_model=Audiology, model=FrasesRepetidas,
                                                                     form=EstFrasesRepetidas, extra=1, max_num=1,
                                                                     can_delete=False, )


class EstEscucha(forms.ModelForm):
    class Meta:
        model = Escucha
        fields = '__all__'


estado_actual_escucha_section = forms.inlineformset_factory(parent_model=Audiology, model=Escucha, form=EstEscucha,
                                                            extra=1, max_num=1, can_delete=False, )


class EstEscuchaRuido(forms.ModelForm):
    class Meta:
        model = EscuchaRuido
        fields = '__all__'


estado_actual_escucha_ruido_section = forms.inlineformset_factory(parent_model=Audiology, model=EscuchaRuido,
                                                                  form=EstEscuchaRuido, extra=1, max_num=1,
                                                                  can_delete=False, )
