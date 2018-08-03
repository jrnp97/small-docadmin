from django import forms

from docapp.models import Audiometry, Information, Otoscopia


class AudiometriaForm(forms.ModelForm):
    class Meta:
        model = Audiometry
        exclude = ('last_modify', 'exam_type', 'create_by', )

    def save(self, commit=True):
        instance = super(AudiometriaForm, self).save(commit=False)
        instance.exam_type = self.exam_type
        instance.create_by = self.create_by
        if commit:
            instance.save()
        return instance


class InfoForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = '__all__'


information_section = forms.inlineformset_factory(parent_model=Audiometry, model=Information, form=InfoForm, extra=1,
                                                  max_num=1, can_delete=False)


class OtoForm(forms.ModelForm):
    class Meta:
        model = Otoscopia
        fields = '__all__'


otoscopia_section = forms.inlineformset_factory(parent_model=Audiometry, model=Otoscopia, form=OtoForm, extra=1,
                                                max_num=1, can_delete=False)
