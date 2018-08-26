from django import forms

from docapp.models import (Audiology,
                           Ananmesis,
                           AntFamiliares,
                           OtrosAntecedentes,
                           ExposicionAudifonos, ExposicionMotocicleta, ExposicionAutomotriz, ExposicionMaquinariaPesada,
                           RuidoMolestia, VolumenTv, FrasesRepetidas, Escucha, EscuchaRuido,
                           Audiometria)


class AudioForm(forms.ModelForm):
    class Meta:
        model = Audiology
        exclude = ('ultima_vez_modificado', 'tipo_examen', )

    def save(self, commit=True):
        instance = super(AudioForm, self).save(commit=False)
        instance.tipo_examen = self.exam_type
        if commit:
            instance.save()
        return instance


ananmesis_section = forms.inlineformset_factory(parent_model=Audiology, model=Ananmesis, extra=1, max_num=1,
                                                can_delete=False, fields='__all__')

ant_familiar_section = forms.inlineformset_factory(parent_model=Audiology, model=AntFamiliares, extra=1, max_num=1,
                                                   can_delete=False, fields='__all__')

ant_otro_section = forms.inlineformset_factory(parent_model=Audiology, model=OtrosAntecedentes, extra=1, max_num=1,
                                               can_delete=False, fields='__all__')


class CleanChilds(object):
    def is_valid(self):
        """ Overwrite method is valid (Executed before run bulk_create to check formset information """
        return True


# Exposiciones
class ExpoAudifonos(CleanChilds, forms.ModelForm):
    class Meta:
        model = ExposicionAudifonos
        fields = '__all__'


exposicion_audifonos_section = forms.inlineformset_factory(parent_model=Audiology, model=ExposicionAudifonos,
                                                           form=ExpoAudifonos, extra=1, max_num=1, can_delete=False, )


class ExpoMotocicleta(CleanChilds, forms.ModelForm):
    class Meta:
        model = ExposicionMotocicleta
        fields = '__all__'


exposicion_moto_section = forms.inlineformset_factory(parent_model=Audiology, model=ExposicionMotocicleta,
                                                      form=ExpoMotocicleta, extra=1, max_num=1, can_delete=False, )


class ExpoAutomotriz(CleanChilds, forms.ModelForm):
    class Meta:
        model = ExposicionAutomotriz
        fields = '__all__'


exposicion_auto_section = forms.inlineformset_factory(parent_model=Audiology, model=ExposicionAutomotriz,
                                                      form=ExpoAutomotriz, extra=1, max_num=1, can_delete=False, )


class ExpoMaquinariaPesada(CleanChilds, forms.ModelForm):
    class Meta:
        model = ExposicionMaquinariaPesada
        fields = '__all__'


exposicion_pesada_section = forms.inlineformset_factory(parent_model=Audiology, model=ExposicionMaquinariaPesada,
                                                        form=ExpoMaquinariaPesada, extra=1, max_num=1,
                                                        can_delete=False, )


# Estado Actual
class EstRuidoMolestia(CleanChilds, forms.ModelForm):
    class Meta:
        model = RuidoMolestia
        fields = '__all__'


estado_actual_ruido_molestia_section = forms.inlineformset_factory(parent_model=Audiology, model=RuidoMolestia,
                                                                   form=EstRuidoMolestia,
                                                                   extra=1, max_num=1, can_delete=False, )


class EstVolumenTv(CleanChilds, forms.ModelForm):
    class Meta:
        model = VolumenTv
        fields = '__all__'


estado_actual_volumen_tv_section = forms.inlineformset_factory(parent_model=Audiology, model=VolumenTv,
                                                               form=EstVolumenTv, extra=1,
                                                               max_num=1, can_delete=False, )


class EstFrasesRepetidas(CleanChilds, forms.ModelForm):
    class Meta:
        model = FrasesRepetidas
        fields = '__all__'


estado_actual_frases_repetidas_section = forms.inlineformset_factory(parent_model=Audiology, model=FrasesRepetidas,
                                                                     form=EstFrasesRepetidas, extra=1, max_num=1,
                                                                     can_delete=False, )


class EstEscucha(CleanChilds, forms.ModelForm):
    class Meta:
        model = Escucha
        fields = '__all__'


estado_actual_escucha_section = forms.inlineformset_factory(parent_model=Audiology, model=Escucha, form=EstEscucha,
                                                            extra=1, max_num=1, can_delete=False, )


class EstEscuchaRuido(CleanChilds, forms.ModelForm):
    class Meta:
        model = EscuchaRuido
        fields = '__all__'


estado_actual_escucha_ruido_section = forms.inlineformset_factory(parent_model=Audiology, model=EscuchaRuido,
                                                                  form=EstEscuchaRuido, extra=1, max_num=1,
                                                                  can_delete=False, )

audiometria_section = forms.inlineformset_factory(parent_model=Audiology, model=Audiometria, extra=1, max_num=1,
                                                  can_delete=False, fields='__all__')