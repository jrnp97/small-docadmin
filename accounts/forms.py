from django import forms
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import SuspiciousOperation

from accounts.models import DoctorProfile, LaboratoryProfile, ReceptionProfile

User = get_user_model()


class BaseUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)

    def clean_password2(self):
        # Check if both password match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las Constraseñas no coinciden")
        return password2

    def save(self, commit=True):
        instance = super(BaseUserForm, self).save(commit=False)
        # Set clean password to user to save
        instance.password = self.cleaned_data.get('password2')
        if commit:
            instance.save()
        return instance


class RecAndLabForm(BaseUserForm):
    """ Form to register Receptionist or Laboratory profile if only one because actually don't have different fields"""
    RECP = 'receptionist'
    LAB = 'laboratory'
    PROFILE_TYPE = (
        (RECP, 'Receptionist'),
        (LAB, 'Laboratory')
    )
    profile_type = forms.ChoiceField(choices=PROFILE_TYPE)

    def save(self, commit=True):
        instance = super(RecAndLabForm, self).save(commit=False)
        # Set receptionist profile
        profile = self.cleaned_data.get('profile_type')
        instance.profile_type = profile
        if commit:
            # Save user
            instance.save()
            # Save profile now
            if not self.cleaned_data['profile_type']:
                raise SuspiciousOperation()

            try:
                if profile == self.RECP:
                    ReceptionProfile.objects.create(user=instance)
                elif profile == self.LAB:
                    LaboratoryProfile.objects.create(user=instance)

            except IntegrityError:
                # Delete user
                instance.delete()
                raise forms.ValidationError(message="Unable to save receptionist profile, check information",
                                            code='invalid')
        return instance


class DoctorForm(BaseUserForm):
    """ Form to register doctor """
    general = forms.BooleanField(initial=False, label='General', widget=forms.CheckboxInput, required=False)
    visiometry = forms.BooleanField(initial=False, label='Visiometro', widget=forms.CheckboxInput, required=False)
    audiometry = forms.BooleanField(initial=False, label='Audiometro', widget=forms.CheckboxInput, required=False)
    audiology = forms.BooleanField(initial=False, label='Audiologo', widget=forms.CheckboxInput, required=False)

    def save(self, commit=True):
        instance = super(DoctorForm, self).save(commit=False)
        # Set doctor profile
        instance.profile_type = 'doctor'

        # Make doctorprofile information
        extra_content = {'general': self.cleaned_data.get('general'),
                         'visiometry': self.cleaned_data.get('visiometry'),
                         'audiometry': self.cleaned_data.get('audiometry'),
                         'audiology': self.cleaned_data.get('audiology')}
        if commit:
            # Save user
            instance.save()
            # Save doctor now
            try:
                # Add user to information
                extra_content.update({'user': instance})
                doctor = DoctorProfile(**extra_content)
                # Save doctor
                doctor.save()
            except IntegrityError:
                # Delete user
                instance.delete()
                raise forms.ValidationError(message="Unable to save doctor profile, check information",
                                            code='invalid')
        return instance
