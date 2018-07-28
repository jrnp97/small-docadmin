from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import DoctorForm, RecAndLabForm


# Create your views here.
class Login(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


login = Login.as_view()


class RegisterDoctor(FormView, LoginRequiredMixin):
    form_class = DoctorForm
    template_name = 'accounts/register_profile.html'
    success_url = reverse_lazy('accounts:register_doctor')

    def form_valid(self, form):
        instance = form.save()
        if instance:
            messages.success(request=self.request, message="User created successfully")
        return super(RegisterDoctor, self).form_valid(form)


register_doctor = RegisterDoctor.as_view()


class RegisterRecOrLab(FormView, LoginRequiredMixin):
    form_class = RecAndLabForm
    template_name = 'accounts/register_profile.html'
    success_url = reverse_lazy('accounts:register_rec_or_lab')

    def form_valid(self, form):
        instance = form.save()
        if instance:
            messages.success(request=self.request, message="User created successfully")
        return super(RegisterRecOrLab, self).form_valid(form)


register_rec_or_lab = RegisterRecOrLab.as_view()
