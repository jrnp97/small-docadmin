from django import forms
from docapp.models import Company, Person


class CompanyCreateForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name',
                  'nit',
                  'direction',
                  'land_line',
                  'cellphone',
                  'contact',)
        exclude = ('create_by', )

    def save(self, commit=True):
        instance = super(CompanyCreateForm, self).save(commit=False)
        instance.create_by = self.create_by
        if commit:
            instance.save()
        return instance


class PersonCreateForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = '__all__'
