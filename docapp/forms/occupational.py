from django import forms

from docapp.models.occupational import (Occupational, Ant_familiares, AntecedentGinecoO, Habits, FisicoGeneral,
                                        OrganosSentidos,
                                        Conclusion)


class OcupaForm(forms.ModelForm):
    class Meta:
        model = Occupational
        exclude = ('last_modify', 'exam_type', 'create_by',)

    def save(self, commit=True):
        instance = super(OcupaForm, self).save(commit=False)
        instance.exam_type = self.exam_type
        instance.create_by = self.create_by
        if commit:
            instance.save()
        return instance


class AntFamForm(forms.ModelForm):
    class Meta:
        model = Ant_familiares
        fields = '__all__'


ant_familiares_section = forms.inlineformset_factory(parent_model=Occupational, model=Ant_familiares, form=AntFamForm,
                                                     extra=1, max_num=1, can_delete=False)


class HabiForm(forms.ModelForm):
    class Meta:
        model = Habits
        fields = '__all__'


habitos_section = forms.inlineformset_factory(parent_model=Occupational, model=Habits, form=HabiForm,
                                              extra=1, max_num=1, can_delete=False)

"""
# 
· Gineco section
class SintoForm(forms.ModelForm):
    class Meta:
        model = Sintomas
        fields = '__all__'


sintomas_section = forms.inlineformset_factory(parent_model=Visiometry, model=Sintomas, form=SintoForm,
                                               extra=1, max_num=1, can_delete=False)
"""


class FGeneralForm(forms.ModelForm):
    class Meta:
        model = FisicoGeneral
        fields = '__all__'


fisico_general_form = forms.inlineformset_factory(parent_model=Occupational, model=FisicoGeneral, form=FGeneralForm,
                                                  extra=1, max_num=1, can_delete=False)


class OSentidosForm(forms.ModelForm):
    class Meta:
        model = OrganosSentidos
        fields = '__all__'


organos_sentidos_section = forms.inlineformset_factory(parent_model=Occupational, model=OSentidosForm,
                                                       form=OSentidosForm, extra=1, max_num=1, can_delete=False)


class ConclusionForm(forms.ModelForm):
    class Meta:
        model = Conclusion
        fields = '__all__'


conclusion_section = forms.inlineformset_factory(parent_model=Occupational, model=Conclusion, form=ConclusionForm,
                                                 extra=1, max_num=1, can_delete=False)
