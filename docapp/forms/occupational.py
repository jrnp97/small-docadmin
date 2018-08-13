from django import forms

from docapp.models import (Occupational,
                           AntPersonalesFamiliares,
                           AntGinecoObstetricos,
                           HabitoAlcohol, HabitoCigarrillo, HabitoDroga, HabitoGenerales,
                           ExamFisicoAspectoGeneral, ExamFisicoAbdomen, ExamFisicoBoca, ExamFisicoColumna,
                           ExamFisicoCorazon, ExamFisicoCuello, ExamFisicoExtremidades, ExamFisicoGenitoUnitario,
                           ExamFisicoNariz, ExamFisicoNeurologico, ExamFisicoOidos, ExamFisicoOjos,
                           ExamFisicoToraxPulmones,
                           Conclusion)


class OcupaForm(forms.ModelForm):
    class Meta:
        model = Occupational
        exclude = ('ultima_vez_modificado', 'tipo_examen', 'registrado_por',)

    def save(self, commit=True):
        instance = super(OcupaForm, self).save(commit=False)
        instance.tipo_examen = self.exam_type
        instance.registrado_por = self.create_by
        if commit:
            instance.save()
        return instance


ant_familiares_section = forms.inlineformset_factory(parent_model=Occupational, model=AntPersonalesFamiliares, extra=1,
                                                     max_num=1, can_delete=False, fields='__all__')

ant_gineco_section = forms.inlineformset_factory(parent_model=Occupational, model=AntGinecoObstetricos, extra=1,
                                                 max_num=1, can_delete=False, fields='__all__')

# Habitos
habito_alcohol_section = forms.inlineformset_factory(parent_model=Occupational, model=HabitoAlcohol, extra=1, max_num=1,
                                                     can_delete=False, fields='__all__')

habito_cigarillo_section = forms.inlineformset_factory(parent_model=Occupational, model=HabitoCigarrillo, extra=1,
                                                       max_num=1, can_delete=False, fields='__all__')

habito_droga_section = forms.inlineformset_factory(parent_model=Occupational, model=HabitoDroga, extra=1, max_num=1,
                                                   can_delete=False, fields='__all__')

habito_general_section = forms.inlineformset_factory(parent_model=Occupational, model=HabitoGenerales, extra=1,
                                                     max_num=1, can_delete=False, fields='__all__')
# Examen fisico
examen_fisico_general_section = forms.inlineformset_factory(parent_model=Occupational, model=ExamFisicoAspectoGeneral,
                                                            extra=1, max_num=1, can_delete=False, fields='__all__')

examen_fisico_abdomen_section = forms.inlineformset_factory(parent_model=Occupational, model=ExamFisicoAbdomen, extra=1,
                                                            max_num=1, can_delete=False, fields='__all__')

examen_fisico_boca_section = forms.inlineformset_factory(parent_model=Occupational, model=ExamFisicoBoca, extra=1,
                                                         max_num=1, can_delete=False, fields='__all__')

examen_fisico_columna_section = forms.inlineformset_factory(parent_model=Occupational, model=ExamFisicoColumna, extra=1,
                                                            max_num=1, can_delete=False, fields='__all__')

examen_fisico_corazon_section = forms.inlineformset_factory(parent_model=Occupational, model=ExamFisicoCorazon, extra=1,
                                                            max_num=1, can_delete=False, fields='__all__')

examen_fisico_cuello_section = forms.inlineformset_factory(parent_model=Occupational, model=ExamFisicoCuello, extra=1,
                                                           max_num=1, can_delete=False, fields='__all__')

examen_fisico_extremidades_section = forms.inlineformset_factory(parent_model=Occupational,
                                                                 model=ExamFisicoExtremidades, extra=1, max_num=1,
                                                                 can_delete=False, fields='__all__')

examen_fisico_genito_unitario_section = forms.inlineformset_factory(parent_model=Occupational,
                                                                    model=ExamFisicoGenitoUnitario, extra=1, max_num=1,
                                                                    can_delete=False, fields='__all__')

examen_fisico_nariz_section = forms.inlineformset_factory(parent_model=Occupational, model=ExamFisicoNariz, extra=1,
                                                          max_num=1, can_delete=False, fields='__all__')

examen_fisico_neurologico_section = forms.inlineformset_factory(parent_model=Occupational, model=ExamFisicoNeurologico,
                                                                extra=1, max_num=1, can_delete=False, fields='__all__')

examen_fisico_oidos_section = forms.inlineformset_factory(parent_model=Occupational, model=ExamFisicoOidos, extra=1,
                                                        max_num=1, can_delete=False, fields='__all__')

examen_fisico_ojos_section = forms.inlineformset_factory(parent_model=Occupational, model=ExamFisicoOjos, extra=1,
                                                         max_num=1, can_delete=False, fields='__all__')

examen_fisico_torax_pulmones_section = forms.inlineformset_factory(parent_model=Occupational,
                                                                   model=ExamFisicoToraxPulmones, extra=1, max_num=1,
                                                                   can_delete=False, fields='__all__')
# Fin examen fisico

conclusion_section = forms.inlineformset_factory(parent_model=Occupational, model=Conclusion, extra=1, max_num=1,
                                                 can_delete=False, fields='__all__')
