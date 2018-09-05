from django.shortcuts import redirect
from django.views.generic import FormView, ListView, UpdateView, DetailView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponseRedirect

from docapp.forms import (CompanyForm, PacienteEmpresaForm, PacienteParticularForm,
                          ExaminacionCreateForm, lab_exam_inlineformset, simple_exam_inlineformset,
                          AntLaboralesForm, hazards_inlineformset, accident_inlineformset)

from docapp.models import (Empresa, PacienteEmpresa, PacienteParticular, Examinacion, AntecedentesLaborales, Riesgos,
                           Accidentes, Consulta)

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


# Process Companies
class RegisterCompany(CheckReceptionist, LoginRequiredMixin, FormView):
    form_class = CompanyForm
    template_name = 'docapp/register/company.html'
    success_url = reverse_lazy('docapp:list_company')

    def form_valid(self, form):
        # Add Create_by
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Empresa registrada existosamente")
        return super(RegisterCompany, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['detail'] = 'Empresas'
        return super(RegisterCompany, self).get_context_data(**kwargs)


register_company = RegisterCompany.as_view()


class UpdateCompany(CheckReceptionist, LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'company_id'
    context_object_name = 'company'
    model = Empresa
    form_class = CompanyForm
    template_name = 'docapp/register/company.html'
    success_url = reverse_lazy('docapp:list_company')

    def form_valid(self, form):
        # Add Create_by
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Empresa actualizada existosamente")
        return super(UpdateCompany, self).form_valid(form)


update_company = UpdateCompany.as_view()


class DetailCompany(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'company_id'
    model = Empresa
    context_object_name = 'company'
    template_name = 'docapp/details/company.html'


detail_company = DetailCompany.as_view()


class ListCompanies(CheckReceptionist, LoginRequiredMixin, ListView):
    """ View to list companies """
    context_object_name = 'company_list'
    model = Empresa
    template_name = 'docapp/lists/company_list.html'


list_company = ListCompanies.as_view()


# End process companies


# Process employ from a company
class RegisterEmployFromCompany(CheckReceptionist, LoginRequiredMixin, FormViewPutExtra):
    pk_url_kwarg = 'company_id'
    form_class = PacienteEmpresaForm
    model = PacienteEmpresa
    template_name = 'docapp/register/employ.html'
    success_url = reverse_lazy('docapp:list_company')
    model_to_filter = Empresa

    def form_valid(self, form):
        company = self.get_object()
        form.company = company
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona registrada exitosamente")
        return super(RegisterEmployFromCompany, self).form_valid(form)


register_employ_from_company = RegisterEmployFromCompany.as_view()


class ListEmpleadosEmpresa(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'company_id'
    context_object_name = 'company'
    model = Empresa
    template_name = 'docapp/lists/person_list_company.html'


list_employ_company = ListEmpleadosEmpresa.as_view()


# End process employ from a company


# Process employ without company
class RegisterEmployWithoutCompany(CheckReceptionist, LoginRequiredMixin, FormView):
    form_class = PacienteEmpresaForm
    model = PacienteEmpresa
    template_name = 'docapp/register/employ.html'
    success_url = reverse_lazy('docapp:list_company')

    def form_valid(self, form):
        form.company = None
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona registrada exitosamente")
        return super(RegisterEmployWithoutCompany, self).form_valid(form)


register_employ_without_company = RegisterEmployWithoutCompany.as_view()


class ListEmplotWithoutCompany(CheckReceptionist, LoginRequiredMixin, ListView):
    context_object_name = 'person_list'
    model = PacienteEmpresa
    queryset = PacienteEmpresa.objects.filter(empresa=None)
    template_name = 'docapp/lists/person_list.html'


list_independent_employ = ListEmplotWithoutCompany.as_view()


# End process employ without company


# Views general to employs (with company or without company)
class UpdateEmploy(CheckReceptionist, LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'person_id'
    context_object_name = 'person'
    model = PacienteEmpresa
    form_class = PacienteEmpresaForm
    template_name = 'docapp/register/employ.html'
    success_url = reverse_lazy('docapp:list_company')

    def form_valid(self, form):
        person = self.get_object()
        form.create_by = self.request.user.reception_profile
        form.company = person.empresa
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona actualizada existosamente")
        return super(UpdateEmploy, self).form_valid(form)


update_employ = UpdateEmploy.as_view()


class DetailEmploy(CheckRecOrDoc, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'person_id'
    model = PacienteEmpresa
    context_object_name = 'person'
    template_name = 'docapp/details/person.html'


detail_employ = DetailEmploy.as_view()


# End views general to employs (with company or without company)


# Process employ antecedent
class RegisterEmployAntecedent(CheckReceptionist, LoginRequiredMixin, FormsetPostManager, FormViewPutExtra):
    pk_url_kwarg = 'person_id'
    form_class = AntLaboralesForm
    model = AntecedentesLaborales
    template_name = 'docapp/register/antecedent.html'
    success_url = reverse_lazy('docapp:dashboard')
    model_to_filter = PacienteEmpresa
    context_object_2_name = 'person'
    extra_context = {'exam_name': 'Antecedente',
                     'parent_object_key': 'antecedente_id',
                     'formsets': [
                         {'section_name': 'riesgos',
                          'title': 'Riesgos',
                          'form': hazards_inlineformset},
                         {'section_name': 'accidentes',
                          'title': 'Accidentes',
                          'form': accident_inlineformset}
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


register_employ_antecedent = RegisterEmployAntecedent.as_view()


class UpdateEmployAntecedent(CheckReceptionist, LoginRequiredMixin, FormsetPostManager, UpdateView):
    pk_url_kwarg = 'antecedent_id'
    context_object_name = 'antecedent'
    model = AntecedentesLaborales
    form_class = AntLaboralesForm
    template_name = 'docapp/register/antecedent.html'
    success_url = reverse_lazy('docapp:dashboard')
    extra_context = {'parent_object_key': 'antecedente_id',
                     'formsets': [
                         {'section_name': 'riesgos',
                          'title': 'Riesgos',
                          'form': hazards_inlineformset},
                         {'section_name': 'accidentes',
                          'title': 'Accidentes',
                          'form': accident_inlineformset}
                     ]
                     }

    def form_valid(self, form):
        """ Overwrite form_valid to add missing information"""
        antecedent = self.get_object()
        form.create_by = self.request.user.reception_profile
        form.person = antecedent.person
        return super(UpdateEmployAntecedent, self).form_valid(form)

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
        # TODO add get information from accidents
        self.extra_context = {'parent_object_key': 'antecedente_id',
                              'formsets': [
                                  {'section_name': 'riesgos',
                                   'title': 'Riesgos',
                                   'form': hazards_inlineformset(initial=hazard_initial_data)}
                              ]
                              }
        kwargs.update(self.extra_context)
        return super(UpdateEmployAntecedent, self).get_context_data(**kwargs)


update_employ_antecedent = UpdateEmployAntecedent.as_view()


class ListEmployAntecedents(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'person_id'
    context_object_name = 'paciente'
    model = PacienteEmpresa
    template_name = 'docapp/lists/antecedent_list.html'


list_employ_antecedents = ListEmployAntecedents.as_view()


class DetailEmployAntecedent(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'antecedent_id'
    model = AntecedentesLaborales
    context_object_name = 'antecedent'
    template_name = 'docapp/details/antecedent.html'


detail_employ_antecedent = DetailEmployAntecedent.as_view()


# End employ antecedent


# Process Employ Examinations
class RegisterEmployExamination(CheckReceptionist, LoginRequiredMixin, FormsetPostManager, FormViewPutExtra):
    pk_url_kwarg = 'person_id'
    model = Examinacion
    form_class = ExaminacionCreateForm
    model_to_filter = PacienteEmpresa
    context_object_2_name = 'person'
    success_url = reverse_lazy('docapp:list_examination')
    template_name = 'docapp/register/examination.html'
    extra_context = {'parent_object_key': 'examinacion_id',
                     'formsets': [
                         {'section_name': 'inter_exam',
                          'title': 'Examenes Internos',
                          'form': simple_exam_inlineformset},
                         {'section_name': 'lab_exams',
                          'title': 'Examenes de Laboratorio',
                          'form': lab_exam_inlineformset}
                     ]
                     }

    def _custom_save(self, form):
        person = self.get_object()
        form.create_by = self.request.user.reception_profile
        form.person = person
        instance = form.save()
        if instance:
            person_name = person.__str__()
            messages.success(self.request, message=f"Antecedente de {person_name} register exitosamente")
        return instance

register_employ_examination = RegisterEmployExamination.as_view()


class ListExamination(LoginRequiredMixin, CheckUser, ListView):
    model = Examinacion
    context_object_name = 'exam_list'
    template_name = 'docapp/lists/exam_list.html'


list_examination = ListExamination.as_view()


# End process examinations


# Process particular
class RegisterParticular(CheckReceptionist, LoginRequiredMixin, FormView):
    form_class = PacienteParticularForm
    model = PacienteParticular
    template_name = 'docapp/register/simple_patient.html'
    success_url = reverse_lazy('docapp:list_simple_patient')

    def form_valid(self, form):
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona registrada exitosamente")
        return super(RegisterParticular, self).form_valid(form)


register_simple_patient = RegisterParticular.as_view()


class UpdateParticular(CheckReceptionist, LoginRequiredMixin, UpdateView):
    context_object_name = 'patient'
    model = PacienteParticular
    form_class = PacienteParticularForm
    template_name = 'docapp/register/simple_patient.html'
    success_url = reverse_lazy('docapp:list_simple_patient')

    def form_valid(self, form):
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona actualizada existosamente")
        return super(UpdateParticular, self).form_valid(form)


update_simple_patient = UpdateParticular.as_view()


class ListParticular(CheckUser, LoginRequiredMixin, ListView):
    model = PacienteParticular
    template_name = 'docapp/lists/simple_patient.html'
    context_object_name = 'patient_list'


list_simple_patient = ListParticular.as_view()


class DetailParticular(CheckRecOrDoc, LoginRequiredMixin, DetailView):
    model = PacienteParticular
    template_name = 'docapp/details/simple_patient.html'
    context_object_name = 'patient'


detail_patient = DetailParticular.as_view()


# End process particular


# Process consult
@login_required
@require_POST
@user_passes_test(test_func=(lambda u: hasattr(u, 'reception_profile') or u.is_superuser),
                  login_url=reverse_lazy('docapp:dashboard'))
def make_consulta(request, patient_id):
    try:
        patient = PacienteParticular.objects.get(pk=patient_id)
    except ObjectDoesNotExist:
        return Http404("El paciente no se encuentra registrado")
    else:
        Consulta(registrado_por=request.user.reception_profile, paciente_id=patient).save()
        return HttpResponseRedirect(reverse_lazy('docapp:list_simple_patient'), status=200)


class ListConsultas(CheckUser, LoginRequiredMixin, ListView):
    model = Consulta
    context_object_name = 'consult_list'
    template_name = 'docapp/lists/consult_list.html'


list_consults = ListConsultas.as_view()
# End process consult
