from django.shortcuts import redirect
from django.forms import model_to_dict
from django.views.generic import FormView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured

from accounts.forms import (BaseUserForm, BaseUserUpdateForm)
from accounts.models import User, DoctorProfile, ReceptionProfile, LaboratoryProfile


# Create your views here.
class Login(LoginView):
    """ View to login """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


login = Login.as_view()
logout = LogoutView.as_view()


# Check permissions user
class CheckSuperUser(UserPassesTestMixin):
    def handle_no_permission(self):
        """ Redirect to user dashboard if no't satisfy Test"""
        return redirect('docapp:dashboard')

    def test_func(self):
        """ Check if user is superuser """
        return self.request.user.is_superuser


class RegisterPersonal(LoginRequiredMixin, CheckSuperUser, FormView):
    form_class = BaseUserForm
    template_name = 'accounts/register_profile.html'
    success_url = reverse_lazy('accounts:register_personal')

    def form_valid(self, form):
        instance = form.save()
        if instance:
            messages.success(request=self.request, message="User created successfully")
        return super(RegisterPersonal, self).form_valid(form)


register_personal = RegisterPersonal.as_view()


class UpdatePersonal(LoginRequiredMixin, CheckSuperUser, UpdateView):
    """ View to update doctor profile """
    pk_url_kwarg = 'user_id'
    model = User
    template_name = 'accounts/register_profile.html'
    form_class = BaseUserUpdateForm
    success_url = reverse_lazy('accounts:register_personal')

    def form_valid(self, form):
        messages.success(request=self.request, message="Doctor profile update successfully")
        return super(UpdatePersonal, self).form_valid(form)


update_personal = UpdatePersonal.as_view()


class DeletePersonal(LoginRequiredMixin, CheckSuperUser, DeleteView):
    """ View to 'delete' doctor profile """
    pk_url_kwarg = 'user_id'
    context_object_name = 'instance'
    model = User
    template_name = 'accounts/delete_profile.html'
    success_url = reverse_lazy('accounts:login')


delete_personal = DeletePersonal.as_view()


class DetailPersonal(LoginRequiredMixin, CheckSuperUser, DetailView):
    pk_url_kwarg = 'user_id'
    context_object_name = 'instance'
    model = User
    template_name = 'accounts/show_profile.html'


detail_personal = DetailPersonal.as_view()


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
                "User information is bad configure"
            )
        self.form_class = BaseUserUpdateForm
        return super(UpdateProfile, self).get_form_class()


update_profile = UpdateProfile.as_view()


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
