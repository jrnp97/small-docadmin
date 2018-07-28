from django.contrib import admin
from accounts.models import User
from accounts.forms import DoctorForm
# Register your models here.


class DoctorAdmin(admin.ModelAdmin):
    form = DoctorForm


admin.site.register(User, DoctorAdmin)
