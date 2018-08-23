from django.contrib import admin
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from accounts.models import User, ReceptionProfile, DoctorProfile
from labapp.models import LaboratoryProfile
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        fields = '__all__'

    def save_model(self, request, obj, form, change):
        # Save current model (User)
        super(UserAdmin, self).save_model(request, obj, form, change)
        # Save profile now
        try:
            if obj.is_superuser:
                info = {'user_id': obj}
                ReceptionProfile(**info).save()
                # Administrator only can be receptionist profile
            elif obj.profile_type == 'receptionista':
                info = {'user_id': obj}
                reception = ReceptionProfile(**info)
                reception.save()
            elif obj.profile_type == 'p_laboratorio':  # TODO Fix Laboratory user register with stack inline
                info = {'user_id': obj}
                laboratory = LaboratoryProfile(**info)
                laboratory.save()
            elif obj.profile_type == 'doctor':
                info = {'user_id': obj}
                doctor = DoctorProfile(**info)
                # Save doctor
                doctor.save()
        except IntegrityError:
            obj.delete(destroy=True)
            raise ValidationError(message="Unable to save profile, check information", code='invalid')


admin.site.register(User, UserAdmin)
