from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from docapp.forms import CompanyCreateForm
from docapp.models import Company


# Create your views here.
@login_required()
def dashboard(request):
    if request.user.is_staff and request.user.is_superuser:
        return redirect('admin:login')
    else:
        context = dict({
            'routes': ['Inicio'],
            'page_header': 'Dashboard Proof',
            'active': 'inicio',
            'exam_collapse': True,
        })
        return render(request, 'docapp/home.html', context)


# List Views
class CompanyList(LoginRequiredMixin, ListView):
    context_object_name = 'company_list'
    model = Company
    template_name = 'docapp/lists/company_list.html'


company_list = CompanyList.as_view()


# Register Views
class RegisterCompany(LoginRequiredMixin, FormView):
    form_class = CompanyCreateForm
    template_name = 'docapp/register/register_simple_form.html'
    success_url = reverse_lazy('docapp:register_company')

    def form_valid(self, form):
        # Add Create_by
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Empresa registrada existosamente")
        return super(RegisterCompany, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Registro empresa'
        return super(RegisterCompany, self).get_context_data(**kwargs)


register_company = RegisterCompany.as_view()


# Update Views
class UpdateCompany(LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'company_id'
    context_object_name = 'company'
    form_class = CompanyCreateForm
    template_name = 'docapp/register/register_simple_form.html'
    success_url = reverse_lazy('docapp:register_company')

    def form_valid(self, form):
        instance = form.save()
        if instance:
            messages.success(self.request, message="Empresa actualizada existosamente")
        return super(UpdateCompany, self).form_valid(form)


update_company = UpdateCompany.as_view()


# Detail Views
class DetailCompany(LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'company_id'
    model = Company
    context_object_name = 'company'
    template_name = 'docapp/details/company.html'

    def get_context_data(self, **kwargs):
        return super(DetailCompany, self).get_context_data(**kwargs)


detail_company = DetailCompany.as_view()
