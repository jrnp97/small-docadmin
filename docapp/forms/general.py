from django import forms
from django.core.exceptions import ObjectDoesNotExist

from docapp.models import Company, Person, ExamType as Exam, AntecedentJobs, JobAccidents, Hazards


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',
                  'nit',
                  'direction',
                  'land_line',
                  'cellphone',
                  'contact',)
        exclude = ('create_by',)

    def save(self, commit=True):
        instance = super(CompanyForm, self).save(commit=False)
        instance.create_by = self.create_by
        if commit:
            instance.save()
        return instance


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'last_name', 'identification', 'born_place', 'born_date',
                  'sex', 'civil_state', 'number_sons', 'direction', 'land_line',
                  'cellphone', 'occupation', 'position', 'stratus', 'training_student',
                  'sena_learner', 'number_patronal',)
        exclude = ('create_by', 'company',)

    def save(self, commit=True):
        instance = super(PersonForm, self).save(commit=False)
        instance.create_by = self.create_by
        instance.company = self.company
        if commit:
            instance.save()
        return instance


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('name',
                  'state',)
        exclude = ('create_by', 'person',)

    def save(self, commit=True):
        instance = super(ExamForm).save(commit=False)
        instance.create_by = self.creta_by
        # Check if exam doesn't exist before
        try:
            Exam.objects.get(instance)
        except ObjectDoesNotExist:
            # Clean state
            if instance.state != 'pendiente':
                raise forms.ValidationError(
                    message='El estado no puede ser diferente a pendiente, apenas se inicia el proceso',
                    code='invalid'
                )

        if commit:
            instance.save()
        return instance


class AntecedentForm(forms.ModelForm):
    class Meta:
        model = AntecedentJobs
        fields = ('company', 'occupation', 'time', 'uso_epp',)

        exclude = ('create_by', 'person',)

    def save(self, commit=True):
        instance = super(AntecedentForm, self).save(commit=False)
        instance.create_by = self.create_by
        instance.person = self.person
        if commit:
            instance.save()
        return instance


class AntHazardForm(forms.ModelForm):
    class Meta:
        model = Hazards
        fields = ('fisico', 'fisico', 'quimico',
                  'mecanico', 'ergonomico', 'electrico',
                  'electrico', 'psicologico', 'locativo')
        exclude = ('work',)


hazards_inlineformset = forms.inlineformset_factory(parent_model=AntecedentJobs, model=Hazards,
                                                    form=AntHazardForm,
                                                    can_delete=False,
                                                    extra=1,
                                                    max_num=1
                                                    )


class AccidentsForm(forms.ModelForm):
    class Meta:
        model = JobAccidents
        fields = ('secuelas', 'tipo', 'atendido',
                  'calificado', 'fecha', 'description',)
        exclude = ('create_by',)


accidents_formset = forms.modelformset_factory(model=JobAccidents, form=AccidentsForm, can_delete=True)
