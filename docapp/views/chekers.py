from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin


# Permissions checker
class CheckerBase(UserPassesTestMixin):
    def handle_no_permission(self):
        return redirect('docapp:dashboard')

    def test_func(self, **kwargs):
        pass


class CheckReceptionist(CheckerBase):
    def test_func(self):
        return hasattr(self.request.user, 'reception_profile') or self.request.user.is_superuser


class CheckLaboratory(CheckerBase):
    def test_func(self):
        return hasattr(self.request.user, 'laboratory_profile') or self.request.user.is_superuser


class CheckDoctor(CheckerBase):
    def test_func(self):
        return hasattr(self.request.user, 'doctor_profile') or self.request.user.is_superuser


class CheckUser(CheckerBase):
    def test_func(self):
        result = (hasattr(self.request.user, 'reception_profile') or self.request.user.is_superuser or
                  hasattr(self.request.user, 'laboratory_profile') or hasattr(self.request.user, 'doctor_profile'))
        return result


class CheckRecOrDoc(CheckerBase):
    def test_func(self, **kwargs):
        normal_user = hasattr(self.request.user, 'reception_profile') or hasattr(self.request.user, 'doctor_profile')
        return normal_user or self.request.user.is_superuser
