from django import forms
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget

from accounts.models import DoctorProfile, LaboratoryProfile, ReceptionProfile

User = get_user_model()


# Base Creation Form
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


# Profile creation forms
class DoctorCreateForm(BaseUserForm):
    """ Form to register doctor """
    general = forms.BooleanField(initial=False, label='General', widget=forms.CheckboxInput, required=False)
    visiometry = forms.BooleanField(initial=False, label='Visiometro', widget=forms.CheckboxInput, required=False)
    audiometry = forms.BooleanField(initial=False, label='Audiometro', widget=forms.CheckboxInput, required=False)
    audiology = forms.BooleanField(initial=False, label='Audiologo', widget=forms.CheckboxInput, required=False)

    def save(self, commit=True):
        instance = super(DoctorCreateForm, self).save(commit=False)
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


class RecCreateForm(BaseUserForm):
    """ Form to register Receptionist profile"""

    def save(self, commit=True):
        instance = super(RecCreateForm, self).save(commit=False)
        # Set receptionist profile
        instance.profile_type = 'receptionist'
        if commit:
            # Save user
            instance.save()
            # Save receptionist profile now
            try:
                ReceptionProfile.objects.create(user=instance)
                LaboratoryProfile.objects.create(user=instance)
            except IntegrityError:
                # Delete user
                instance.delete()
                raise forms.ValidationError(message="Unable to save receptionist profile, check information",
                                            code='invalid')
        return instance


class LabCreateForm(BaseUserForm):
    """ Form to register Laboratory profile"""

    def save(self, commit=True):
        instance = super(LabCreateForm, self).save(commit=False)
        # Set receptionist profile
        instance.profile_type = 'laboratory'
        if commit:
            # Save user
            instance.save()
            # Save receptionist profile now
            try:
                LaboratoryProfile.objects.create(user=instance)
            except IntegrityError:
                # Delete user
                instance.delete()
                raise forms.ValidationError(message="Unable to save receptionist profile, check information",
                                            code='invalid')
        return instance


# Profile update forms
class DoctorUpdateForm(BaseUserForm):
    """ Form to update doctor profile """
    general = forms.BooleanField(initial=False, label='General', widget=forms.CheckboxInput, required=False)
    visiometry = forms.BooleanField(initial=False, label='Visiometro', widget=forms.CheckboxInput, required=False)
    audiometry = forms.BooleanField(initial=False, label='Audiometro', widget=forms.CheckboxInput, required=False)
    audiology = forms.BooleanField(initial=False, label='Audiologo', widget=forms.CheckboxInput, required=False)

    password1 = None
    password2 = None
    password = forms.CharField(label='password', required=False)

    class Meta(BaseUserForm.Meta):
        # Add password field
        fields = BaseUserForm.Meta.fields + ('password',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        # https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#a-full-example
        return self.initial["password"]

    def save(self, commit=True):
        instance = super(DoctorUpdateForm, self).save(commit=False)
        # Set doctor profile
        instance.profile_type = 'doctor'
        instance.password = self.cleaned_data.get('password')  # Set password without edit
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


class RecUpdateForm(BaseUserForm):
    password1 = None
    password2 = None
    password = forms.CharField(label='password', required=False)

    class Meta(BaseUserForm.Meta):
        # Add password field
        fields = BaseUserForm.Meta.fields + ('password',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        # https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#a-full-example
        return self.initial["password"]

    def save(self, commit=True):
        instance = super(RecUpdateForm, self).save(commit=False)
        # Set receptionist profile
        instance.profile_type = 'receptionist'
        instance.password = self.cleaned_data.get('password')  # Set password without edit
        if commit:
            # Save user
            instance.save()
            # Save receptionist profile now
            try:
                ReceptionProfile.objects.create(user=instance)
                LaboratoryProfile.objects.create(user=instance)
            except IntegrityError:
                # Delete user
                instance.delete()
                raise forms.ValidationError(message="Unable to save receptionist profile, check information",
                                            code='invalid')
        return instance


class LabUpdateForm(BaseUserForm):
    password1 = None
    password2 = None
    password = forms.CharField(label='password', required=False)

    class Meta(BaseUserForm.Meta):
        # Add password field
        fields = BaseUserForm.Meta.fields + ('password',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        # https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#a-full-example
        return self.initial["password"]

    def save(self, commit=True):
        instance = super(LabUpdateForm, self).save(commit=False)
        # Set receptionist profile
        instance.profile_type = 'laboratory'
        instance.password = self.cleaned_data.get('password')  # Set password without edit
        if commit:
            # Save user
            instance.save()
            # Save receptionist profile now
            try:
                LaboratoryProfile.objects.create(user=instance)
            except IntegrityError:
                # Delete user
                instance.delete()
                raise forms.ValidationError(message="Unable to save receptionist profile, check information",
                                            code='invalid')
        return instance
