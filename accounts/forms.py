from django import forms
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.models import DoctorProfile, ReceptionProfile
from accounts.choices import RECP, DOCTOR

User = get_user_model()


# Base Creation Form using to admin profile
class BaseUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme Contraseña', widget=forms.PasswordInput)

    def __init__(self, **kwargs):
        super(BaseUserForm, self).__init__(**kwargs)
        if self.fields.get('profile_type'):
            self.fields['profile_type'].choices.remove(('p_laboratorio', 'Personal de Laboratorio'))  # Delete p_lab option

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_type',)

    def clean_password2(self):
        # Check if both password match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las Constraseñas no coinciden")
        return password2

    def clean_profile_type(self):
        """ If some expert action send p_laboratorio key across http params invalid it"""
        p_profile = self.cleaned_data.get('profile_type')
        if p_profile == 'p_laboratorio':
            raise forms.ValidationError("Opcion Seleccionada no valida")
        return p_profile

    def save(self, commit=True):
        instance = super(BaseUserForm, self).save(commit=False)
        # Set clean password to user to save
        instance.password = self.cleaned_data.get('password2')
        if commit:
            instance.save()
            # Save profile now
            try:
                if instance.profile_type == RECP:
                    info = {'user_id': instance}
                    reception = ReceptionProfile(**info)
                    reception.save()
                elif instance.profile_type == DOCTOR:
                    info = {'user_id': instance}
                    doctor = DoctorProfile(**info)
                    doctor.save()
            except IntegrityError:
                instance.delete(destroy=True)
                raise forms.ValidationError(message="Unable to save profile, check information", code='invalid')
        return instance


class BaseUserUpdateForm(forms.ModelForm):
    password = forms.CharField(label='password', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'password', 'is_active', )
        exclude = ('profile_type',)

    def clean_password(self):
        """ To change password need required to administrator """
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        # https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#a-full-example
        return self.initial["password"]

    def save(self, commit=True):
        instance = super(BaseUserUpdateForm, self).save(commit=False)
        instance.password = self.cleaned_data.get('password')  # Set password without edit
        if commit:
            instance.save()
        return instance


# Create Forms
class DoctorCreateForm(BaseUserForm):
    def save(self, commit=True):
        instance = super(DoctorCreateForm, self).save(commit=False)
        instance.profile_type = 'doctor'  # Set doctor profile
        super(DoctorCreateForm, self).save()  # Now save user


class RecCreateForm(BaseUserForm):
    """ Form to register Receptionist profile """

    def save(self, commit=True):
        instance = super(RecCreateForm, self).save(commit=False)
        instance.profile_type = 'receptionista'  # Set receptionist profile
        super(RecCreateForm, self).save()  # Now save user


# Profile update forms
class DoctorUpdateForm(BaseUserUpdateForm):
    """ Form to update doctor profile if required modify something """


class RecUpdateForm(BaseUserUpdateForm):
    """ Form to update receptionist profile if required modify something """
