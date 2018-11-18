from django.views.generic import FormView, UpdateView, DeleteView, DetailView, ListView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from docproject.helpers import CheckSuperUser
from accounts.forms import (BaseUserForm, BaseUserUpdateForm)
from accounts.models import User
from accounts.choices import RECP, DOCTOR


# Create your views here.
class Login(LoginView):
    """ View to login """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


login = Login.as_view()
logout = LogoutView.as_view()


class RegisterPersonal(LoginRequiredMixin, CheckSuperUser, FormView):
    form_class = BaseUserForm
    template_name = 'accounts/register_profile.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        if form.save():
            messages.success(request=self.request, message="User created successfully")
        return super(RegisterPersonal, self).form_valid(form)


register_personal = RegisterPersonal.as_view()


class UpdatePersonal(LoginRequiredMixin, UpdateView):
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
    success_url = reverse_lazy('accounts:user_list')


delete_personal = DeletePersonal.as_view()


class DetailPersonal(LoginRequiredMixin, CheckSuperUser, DetailView):
    pk_url_kwarg = 'user_id'
    context_object_name = 'instance'
    model = User
    template_name = 'accounts/show_profile.html'


detail_personal = DetailPersonal.as_view()


class DetailProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/session/show_profile.html'

    def get_object(self, **kwargs):
        return self.request.user


show_profile = DetailProfile.as_view()


class UpdateProfile(LoginRequiredMixin, UpdateView):
    """ View to update admin profile """
    pk_url_kwarg = 'user_id'
    model = User
    template_name = 'accounts/session/update_profile.html'
    form_class = BaseUserUpdateForm
    success_url = reverse_lazy('docapp:dashboard')

    def form_valid(self, form):
        messages.success(request=self.request, message="Laboratory Profile Update Successfully")
        return super(UpdateProfile, self).form_valid(form)

    def get_object(self, **kwargs):
        return self.request.user


update_profile = UpdateProfile.as_view()


class UserList(LoginRequiredMixin, ListView):
    context_object_name = 'user_list'
    model = User
    template_name = 'accounts/list_user.html'
    queryset = User.objects.filter(Q(is_superuser=False) & Q(profile_type__in=[DOCTOR, RECP]))

    def get_queryset(self):
        user = self.request.user
        self.queryset = self.queryset.exclude(id=user.id)
        return super(UserList, self).get_queryset()


user_list = UserList.as_view()
