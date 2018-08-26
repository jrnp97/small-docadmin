from django.shortcuts import redirect
from django.views.generic import FormView, ListView, UpdateView, DetailView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from docapp.forms import CompanyForm, PacienteEmpresaForm, AntLaboralesForm, hazards_inlineformset, ExaminacionForm
from docapp.models import Empresa, PacienteEmpresa, AntecedentesLaborales, Riesgos, Examinacion

from docproject.helpers.chekers import CheckReceptionist, CheckUser, CheckRecOrDoc
from docproject.helpers.customs import FormViewPutExtra, FormsetPostManager


# Create your views here.
class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'docapp/dashboard.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff and request.user.is_superuser:
            return redirect('admin:login')
        else:
            return super(Dashboard, self).get(request, *args, **kwargs)


dashboard = Dashboard.as_view()


# List Views
class ListaEmpresas(CheckReceptionist, LoginRequiredMixin, ListView):
    context_object_name = 'company_list'
    model = Empresa
    template_name = 'docapp/lists/company_list.html'


company_list = ListaEmpresas.as_view()


class ListaPersonasIndependientes(CheckReceptionist, LoginRequiredMixin, ListView):
    context_object_name = 'person_list'
    model = PacienteEmpresa
    queryset = PacienteEmpresa.objects.filter(empresa=None)
    template_name = 'docapp/lists/person_list.html'


person_list = ListaPersonasIndependientes.as_view()


class EmpleadosEmpresa(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'company_id'
    context_object_name = 'company'
    model = Empresa
    template_name = 'docapp/lists/person_list_company.html'


filter_person_list = EmpleadosEmpresa.as_view()


class ListaAntecedentesEmpleado(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'person_id'
    context_object_name = 'antecedent_list'
    model = PacienteEmpresa
    template_name = 'docapp/lists/antecedent_list.html'

    def get_context_data(self, **kwargs):
        paciente = self.get_object()
        kwargs.update({'antecedent_list': paciente.antecedentes.all()})
        return super(ListaAntecedentesEmpleado, self).get_context_data(**kwargs)


person_antecedent_list = ListaAntecedentesEmpleado.as_view()


# Register Views
class RegisterEmpresa(CheckReceptionist, LoginRequiredMixin, FormView):
    form_class = CompanyForm
    template_name = 'docapp/register/company.html'
    success_url = reverse_lazy('docapp:company_list')

    def form_valid(self, form):
        # Add Create_by
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Empresa registrada existosamente")
        return super(RegisterEmpresa, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['detail'] = 'Empresas'
        return super(RegisterEmpresa, self).get_context_data(**kwargs)


register_company = RegisterEmpresa.as_view()


class RegisterPerson(CheckReceptionist, LoginRequiredMixin, FormView):
    form_class = PacienteEmpresaForm
    model = PacienteEmpresa
    template_name = 'docapp/register/employ.html'
    success_url = reverse_lazy('docapp:person_list')

    def form_valid(self, form):
        form.company = None
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona registrada exitosamente")
        return super(RegisterPerson, self).form_valid(form)


register_person = RegisterPerson.as_view()


class RegistrarEmleado(CheckReceptionist, LoginRequiredMixin, FormViewPutExtra):
    pk_url_kwarg = 'company_id'
    form_class = PacienteEmpresaForm
    model = PacienteEmpresa
    template_name = 'docapp/register/employ.html'
    success_url = reverse_lazy('docapp:person_list')
    model_to_filter = Empresa

    def form_valid(self, form):
        company = self.get_object()
        form.company = company
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona registrada exitosamente")
        return super(RegistrarEmleado, self).form_valid(form)


register_employ = RegistrarEmleado.as_view()


class RegisterAntecedent(CheckReceptionist, LoginRequiredMixin, FormsetPostManager, FormViewPutExtra):
    pk_url_kwarg = 'person_id'
    form_class = AntLaboralesForm
    model = AntecedentesLaborales
    template_name = 'docapp/register/antecedent.html'
    success_url = reverse_lazy('docapp:person_list')
    model_to_filter = PacienteEmpresa
    context_object_2_name = 'person'
    extra_context = {'exam_name': 'Antecedente',
                     'parent_object_key': 'work',
                     'formsets': [
                         {'section_name': 'riesgos',
                          'title': 'Riesgos',
                          'form': hazards_inlineformset}
                     ]
                     }

    def _custom_save(self, form):
        person = self.get_object()
        form.create_by = self.request.user.reception_profile
        form.person = person
        instance = form.save()
        if instance:
            person_name = person.get_full_name()
            messages.success(self.request, message=f"Antecedente de {person_name} register exitosamente")
        return instance


register_antecedent = RegisterAntecedent.as_view()


# Update Views
class UpdateEmpresa(CheckReceptionist, LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'company_id'
    context_object_name = 'company'
    model = Empresa
    form_class = CompanyForm
    template_name = 'docapp/register/company.html'
    success_url = reverse_lazy('docapp:company_list')

    def form_valid(self, form):
        # Add Create_by
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Empresa actualizada existosamente")
        return super(UpdateEmpresa, self).form_valid(form)


update_company = UpdateEmpresa.as_view()


class UpdatePerson(CheckReceptionist, LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'person_id'
    context_object_name = 'person'
    model = PacienteEmpresa
    form_class = PacienteEmpresaForm
    template_name = 'docapp/register/employ.html'
    success_url = reverse_lazy('docapp:person_list')

    def form_valid(self, form):
        person = self.get_object()
        form.create_by = self.request.user.reception_profile
        form.company = person.company
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona actualizada existosamente")
        return super(UpdatePerson, self).form_valid(form)


update_person = UpdatePerson.as_view()


class UpdateAntecedent(CheckReceptionist, LoginRequiredMixin, FormsetPostManager, UpdateView):
    pk_url_kwarg = 'antecedent_id'
    context_object_name = 'antecedent'
    model = AntecedentesLaborales
    form_class = AntLaboralesForm
    template_name = 'docapp/register/antecedent.html'
    success_url = reverse_lazy('docapp:person_list')
    extra_context = {'parent_object_key': 'work',
                     'formsets': [
                         {'section_name': 'riesgos',
                          'title': 'Riesgos',
                          'form': hazards_inlineformset}
                     ]
                     }

    def form_valid(self, form):
        """ Overwrite form_valid to add missing information"""
        antecedent = self.get_object()
        form.create_by = self.request.user.reception_profile
        form.person = antecedent.person
        return super(UpdateAntecedent, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """ Overwrite get_context_data method to append formset necessary"""
        antecedent = self.get_object()
        try:
            data = Riesgos.objects.get(work=antecedent)
            dict_data = vars(data)
            # Delete unneeded info
            dict_data.pop('_state', None)
            dict_data.pop('id', None)
            hazard_initial_data = [dict_data]
        except ObjectDoesNotExist:
            hazard_initial_data = []
        self.extra_context = {'parent_object_key': 'work',
                              'formsets': [
                                  {'section_name': 'riesgos',
                                   'title': 'Riesgos',
                                   'form': hazards_inlineformset(initial=hazard_initial_data)}
                              ]
                              }
        kwargs.update(self.extra_context)
        return super(UpdateAntecedent, self).get_context_data(**kwargs)


update_antecedent = UpdateAntecedent.as_view()


# Detail Views
class DetailEmpresa(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'company_id'
    model = Empresa
    context_object_name = 'company'
    template_name = 'docapp/details/company.html'


detail_company = DetailEmpresa.as_view()


class DetailPerson(CheckRecOrDoc, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'person_id'
    model = PacienteEmpresa
    context_object_name = 'person'
    template_name = 'docapp/details/person.html'


detail_person = DetailPerson.as_view()


class DetailAntecedent(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'antecedent_id'
    model = AntecedentesLaborales
    context_object_name = 'antecedent'
    template_name = 'docapp/details/antecedent.html'


detail_antecedent = DetailAntecedent.as_view()


class RegisterExam(CheckReceptionist, LoginRequiredMixin, FormViewPutExtra):
    pk_url_kwarg = 'person_id'
    model = Examinacion
    form_class = ExaminacionForm
    model_to_filter = PacienteEmpresa
    context_object_2_name = 'person'
    success_url = reverse_lazy('docapp:exam_list')
    template_name = 'docapp/register/exam.html'

    def form_valid(self, form):
        person = self.get_object()
        form.person = person
        form.create_by = self.request.user.reception_profile
        form.initial = True
        instance = form.save()
        if instance:
            messages.success(self.request, message="Examen registrado exitosamente")
        return super(RegisterExam, self).form_valid(form)


register_exam = RegisterExam.as_view()


class ExamList(LoginRequiredMixin, CheckUser, ListView):
    model = Examinacion
    context_object_name = 'exam_list'
    template_name = 'docapp/lists/exam_list.html'


exam_list = ExamList.as_view()
