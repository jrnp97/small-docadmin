from django import forms

from docapp.models import Laboratory, BloodExam, Exams


class LabForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        exclude = ('last_modify', 'exam_type', 'create_by',)

    def save(self, commit=True):
        instance = super(LabForm, self).save(commit=False)
        instance.exam_type = self.exam_type
        instance.create_by = self.create_by
        if commit:
            instance.save()
        return instance


class BloodEForm(forms.ModelForm):
    class Meta:
        model = BloodExam
        fields = '__all__'


blood_section = forms.inlineformset_factory(parent_model=Laboratory, model=BloodExam, form=BloodEForm, extra=1,
                                            max_num=1, can_delete=False)


class ExamsForm(forms.ModelForm):
    class Meta:
        model = Exams
        fields = '__all__'


exams_section = forms.inlineformset_factory(parent_model=Laboratory, model=Exams, form=ExamsForm, extra=1, max_num=1,
                                        can_delete=False)
