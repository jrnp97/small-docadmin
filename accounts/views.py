from django.forms import model_to_dict
from django.views.generic import FormView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured

from accounts.forms import (DoctorCreateForm, RecCreateForm, LabCreateForm,
                            DoctorUpdateForm, RecUpdateForm, LabUpdateForm, BaseUserUpdateForm)
from accounts.models import User, DoctorProfile, ReceptionProfile, LaboratoryProfile


# Create your views here.
class Login(LoginView):
    """ View to login """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


login = Login.as_view()
logout = LogoutView.as_view()


# Register Views
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


# Update Views
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


class UpdateProfile(LoginRequiredMixin, UpdateView):
    """ View to update admin profile """
    pk_url_kwarg = 'user_id'
    model = User
    template_name = 'accounts/session/update_profile.html'
    form_class = None
    success_url = reverse_lazy('docapp:dashboard')

    def form_valid(self, form):
        messages.success(request=self.request, message="Laboratory Profile Update Successfully")
        return super(UpdateProfile, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.id == int(kwargs.get('user_id')):
            return super(UpdateProfile, self).get(request, *args, **kwargs)
        else:
            raise SuspiciousOperation(message="Invalid request")

    def get_form_class(self):
        """ Overwriting function to set correct form class depend of profile_type """
        user = self.get_object()
        # Check user integrity
        if user.is_superuser and user.profile_type is not None:
            raise ImproperlyConfigured(
                "User information is bad confured"
            )

        if user.is_superuser:
            self.form_class = BaseUserUpdateForm
        elif user.profile_type == 'doctor':
            self.form_class = DoctorUpdateForm
        elif user.profile_type == 'receptionist':
            self.form_class = RecUpdateForm
        elif user.profile_type == 'laboratory':
            self.form_class = LabUpdateForm

        return super(UpdateProfile, self).get_form_class()


update_profile = UpdateProfile.as_view()


# Delete Views
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


class DeleteProfile(LoginRequiredMixin, DeleteView):
    pk_url_kwarg = 'user_id'
    context_object_name = 'instance'
    model = User
    template_name = 'accounts/session/delete_profile.html'
    success_url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        if request.user.id == int(kwargs.get('user_id')):
            return super(DeleteProfile, self).get(request, *args, **kwargs)
        else:
            raise SuspiciousOperation(message="Invalid request")


delete_profile = DeleteProfile.as_view()


# Detail views
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


class DetailProfile(LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'user_id'
    model = User
    template_name = 'accounts/session/show_profile.html'

    def get(self, request, *args, **kwargs):
        if request.user.id == int(kwargs.get('user_id')):
            return super(DetailProfile, self).get(request, *args, **kwargs)
        else:
            raise SuspiciousOperation(message="Invalid Request")


show_profile = DetailProfile.as_view()


class UserList(LoginRequiredMixin, ListView):
    context_object_name = 'user_list'
    model = User
    template_name = 'accounts/list_user.html'
    queryset = User.objects.filter(is_superuser=False)

    def get_queryset(self):
        user = self.request.user
        self.queryset = self.queryset.exclude(id=user.id)
        return super(UserList, self).get_queryset()


user_list = UserList.as_view()
