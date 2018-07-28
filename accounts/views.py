from django.forms import model_to_dict
from django.views.generic import FormView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import (DoctorCreateForm, RecCreateForm, LabCreateForm,
                            DoctorUpdateForm, RecUpdateForm, LabUpdateForm)
from accounts.models import User, DoctorProfile, ReceptionProfile, LaboratoryProfile


# Create your views here.
class Login(LoginView):
    """ View to login """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


login = Login.as_view()
logout = LogoutView.as_view()


class RegisterDoctor(LoginRequiredMixin, FormView):
    """ View to register Doctor profile """
    form_class = DoctorCreateForm
    template_name = 'accounts/register_profile.html'
    success_url = reverse_lazy('accounts:register_doctor')

    def form_valid(self, form):
        instance = form.save()
        if instance:
            messages.success(request=self.request, message="User created successfully")
        return super(RegisterDoctor, self).form_valid(form)


register_doctor = RegisterDoctor.as_view()


class RegisterRec(LoginRequiredMixin, FormView):
    """ View to register Receptionist profile """
    form_class = RecCreateForm
    template_name = 'accounts/register_profile.html'
    success_url = reverse_lazy('accounts:register_rec')

    def form_valid(self, form):
        instance = form.save()
        if instance:
            messages.success(request=self.request, message="User created successfully")
        return super(RegisterRec, self).form_valid(form)


register_rec = RegisterRec.as_view()


class RegisterLab(LoginRequiredMixin, FormView):
    """ View to register laboratory profile """
    form_class = LabCreateForm
    template_name = 'accounts/register_profile.html'
    success_url = reverse_lazy('accounts:register_lab')

    def form_valid(self, form):
        instance = form.save()
        if instance:
            messages.success(request=self.request, message="User created successfully")
        return super(RegisterLab, self).form_valid(form)


register_lab = RegisterLab.as_view()


class UpdateDoctor(LoginRequiredMixin, UpdateView):
    """ View to update doctor profile """
    pk_url_kwarg = 'user_id'
    model = User
    template_name = 'accounts/register_profile.html'
    form_class = DoctorUpdateForm
    success_url = reverse_lazy('accounts:register_doctor')

    def get_initial(self):
        """ Overwriting method that return form data so add doctor profile information """
        user = self.get_object()
        doctor_info = DoctorProfile.objects.get(user=user)
        initial_extra = model_to_dict(doctor_info)
        # Delete user unneeded info
        initial_extra.pop('user', None)
        return initial_extra.copy()

    def form_valid(self, form):
        messages.success(request=self.request, message="Doctor profile update successfully")
        return super(UpdateDoctor, self).form_valid(form)


update_doctor = UpdateDoctor.as_view()


class UpdateRec(LoginRequiredMixin, UpdateView):
    """ View to update receptionist profile """
    pk_url_kwarg = 'user_id'
    model = User
    template_name = 'accounts/register_profile.html'
    form_class = RecUpdateForm
    success_url = reverse_lazy('accounts:register_rec')

    def form_valid(self, form):
        messages.success(request=self.request, message="Receptionist profile update successfully")
        return super(UpdateRec, self).form_valid(form)


update_rec = UpdateRec.as_view()


class UpdateLab(LoginRequiredMixin, UpdateView):
    """ View to update laboratory profile """
    pk_url_kwarg = 'user_id'
    model = User
    template_name = 'accounts/register_profile.html'
    form_class = LabUpdateForm
    success_url = reverse_lazy('accounts:register_lab')

    def form_valid(self, form):
        messages.success(request=self.request, message="Laboratory Profile Update Successfully")
        return super(UpdateLab, self).form_valid(form)


update_lab = UpdateLab.as_view()


class DeleteDoctor(LoginRequiredMixin, DeleteView):
    """ View to 'delete' doctor profile """
    pk_url_kwarg = 'user_id'
    context_object_name = 'instance'
    model = DoctorProfile
    template_name = 'accounts/delete_profile.html'
    success_url = reverse_lazy('accounts:login')


delete_doctor = DeleteDoctor.as_view()


class DeleteRec(LoginRequiredMixin, DeleteView):
    """ View to 'delete' receptionist profile """
    pk_url_kwarg = 'user_id'
    context_object_name = 'instance'
    model = ReceptionProfile
    template_name = 'accounts/delete_profile.html'
    success_url = reverse_lazy('accounts:login')


delete_rec = DeleteRec.as_view()


class DeleteLab(LoginRequiredMixin, DeleteView):
    """ View to 'delete' laboratory profile """
    pk_url_kwarg = 'user_id'
    context_object_name = 'instance'
    model = LaboratoryProfile
    template_name = 'accounts/delete_profile.html'
    success_url = reverse_lazy('accounts:login')


delete_lab = DeleteLab.as_view()


class DetailDoctor(LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'user_id'
    context_object_name = 'instance'
    model = DoctorProfile
    template_name = 'accounts/show_profile.html'


show_doctor = DetailDoctor.as_view()


class DetailRec(LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'user_id'
    context_object_name = 'instance'
    model = ReceptionProfile
    template_name = 'accounts/show_profile.html'


show_rec = DetailRec.as_view()


class DetailLab(LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'user_id'
    context_object_name = 'instance'
    model = LaboratoryProfile
    template_name = 'accounts/show_profile.html'


show_lab = DetailLab.as_view()

