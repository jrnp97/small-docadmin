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
                info = {'user': obj}
                ReceptionProfile(**info).save()
                # Administrator only can be receptionist profile
            elif obj.profile_type == 'receptionist':
                info = {'user': obj}
                reception = ReceptionProfile(**info)
                reception.save()
            elif obj.profile_type == 'laboratory':
                info = {'user': obj}
                laboratory = LaboratoryProfile(**info)
                laboratory.save()
            elif obj.profile_type == 'doctor':
                info = {'user': obj}
                doctor = DoctorProfile(**info)
                # Save doctor
                doctor.save()
        except IntegrityError:
            obj.delete(destroy=True)
            raise ValidationError(message="Unable to save profile, check information", code='invalid')


admin.site.register(User, UserAdmin)
