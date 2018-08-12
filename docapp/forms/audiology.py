from django import forms

from docapp.models import (Audiology,
                           Ananmesis,
                           AntFamiliares,
                           OtrosAntecedentes,
                           Exposiciones, ExposicionAudifonos, ExposicionMotocicleta, ExposicionAutomotriz, ExposicionMaquinariaPesada,
                           EstadoActual, RuidoMolestia, VolumenTv, FrasesRepetidas, Escucha, EscuchaRuido,
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
class ExpoAudifonos(CleanChilds, forms.ModelForm):
    class Meta:
        model = ExposicionAudifonos
        fields = '__all__'


exposicion_audifonos_section = forms.inlineformset_factory(parent_model=Exposiciones, model=ExposicionAudifonos,
                                                           form=ExpoAudifonos, extra=1, max_num=1, can_delete=False, )


class ExpoMotocicleta(CleanChilds, forms.ModelForm):
    class Meta:
        model = ExposicionMotocicleta
        fields = '__all__'


exposicion_moto_section = forms.inlineformset_factory(parent_model=Exposiciones, model=ExposicionMotocicleta,
                                                      form=ExpoMotocicleta, extra=1, max_num=1, can_delete=False, )


class ExpoAutomotriz(CleanChilds, forms.ModelForm):
    class Meta:
        model = ExposicionAutomotriz
        fields = '__all__'


exposicion_auto_section = forms.inlineformset_factory(parent_model=Exposiciones, model=ExposicionAutomotriz,
                                                      form=ExpoAutomotriz, extra=1, max_num=1, can_delete=False, )


class ExpoMaquinariaPesada(CleanChilds, forms.ModelForm):
    class Meta:
        model = ExposicionMaquinariaPesada
        fields = '__all__'


exposicion_pesada_section = forms.inlineformset_factory(parent_model=Exposiciones, model=ExposicionMaquinariaPesada,
                                                        form=ExpoMaquinariaPesada, extra=1, max_num=1,
                                                        can_delete=False, )


# Estado Actual
class EstRuidoMolestia(CleanChilds, forms.ModelForm):
    class Meta:
        model = RuidoMolestia
        fields = '__all__'


estado_actual_ruido_molestia_section = forms.inlineformset_factory(parent_model=EstadoActual, model=RuidoMolestia,
                                                                   form=EstRuidoMolestia,
                                                                   extra=1, max_num=1, can_delete=False, )


class EstVolumenTv(CleanChilds, forms.ModelForm):
    class Meta:
        model = VolumenTv
        fields = '__all__'


estado_actual_volumen_tv_section = forms.inlineformset_factory(parent_model=EstadoActual, model=VolumenTv,
                                                               form=EstVolumenTv, extra=1,
                                                               max_num=1, can_delete=False, )


class EstFrasesRepetidas(CleanChilds, forms.ModelForm):
    class Meta:
        model = FrasesRepetidas
        fields = '__all__'


estado_actual_frases_repetidas_section = forms.inlineformset_factory(parent_model=EstadoActual, model=FrasesRepetidas,
                                                                     form=EstFrasesRepetidas, extra=1, max_num=1,
                                                                     can_delete=False, )


class EstEscucha(CleanChilds, forms.ModelForm):
    class Meta:
        model = Escucha
        fields = '__all__'


estado_actual_escucha_section = forms.inlineformset_factory(parent_model=EstadoActual, model=Escucha, form=EstEscucha,
                                                            extra=1, max_num=1, can_delete=False, )


class EstEscuchaRuido(CleanChilds, forms.ModelForm):
    class Meta:
        model = EscuchaRuido
        fields = '__all__'


estado_actual_escucha_radio_section = forms.inlineformset_factory(parent_model=EstadoActual, model=EscuchaRuido,
                                                                  form=EstEscuchaRuido, extra=1, max_num=1,
                                                                  can_delete=False, )
