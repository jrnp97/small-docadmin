from django.contrib import admin
from accounts.models import User, DoctorProfile, ReceptionProfile, LaboratoryProfile
# Register your models here.


admin.site.register(User)
admin.site.register(DoctorProfile)
admin.site.register(ReceptionProfile)
admin.site.register(LaboratoryProfile)
