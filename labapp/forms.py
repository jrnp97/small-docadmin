from django import forms
from django.db import IntegrityError

from accounts.forms import BaseUserForm

from labapp.models import Laboratorio, LaboratoryProfile


class BaseLabUserCreateForm(BaseUserForm):

    class Meta(BaseUserForm.Meta):
        exclude = ('profile_type', )

    def save(self, commit=True, **info):
        instance = super(BaseUserForm, self).save(commit=False)
        # Set clean password to user to save
        instance.password = self.cleaned_data.get('password2')
        instance.profile_type = 'p_laboratorio'  # Set laboratory profile
        if commit:
            instance.save()
            # Save profile now
            try:
                info.update({'user_id': instance})
                laboratory = LaboratoryProfile(**info)
                laboratory.save()
            except IntegrityError:
                instance.delete(destroy=True)
                raise forms.ValidationError(message="Unable to save profile, check information", code='invalid')
        return instance
