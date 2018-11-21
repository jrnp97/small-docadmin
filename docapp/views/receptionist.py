from django.contrib.messages.views import SuccessMessageMixin
from django.db.utils import IntegrityError
from django.shortcuts import redirect
from django.views.generic import FormView, ListView, UpdateView, DetailView, TemplateView, CreateView, View, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse

from docapp.forms import (CompanyForm, PacienteEmpresaForm, PacienteParticularForm,
                          ExaminacionCreateForm, lab_exam_inlineformset, simple_exam_inlineformset)
from labapp.forms import BaseLabUserCreateForm
from accounts.forms import BaseUserUpdateForm

from docapp.models import (Empresa, PacienteEmpresa, PacienteParticular, Examinacion, Consulta)
from labapp.models import Laboratorio, LaboratoryProfile
from accounts.models import User

from docproject.helpers.chekers import CheckReceptionist, CheckUser, CheckRecOrDoc
from docproject.helpers.customs import FormViewPutExtra, FormsetPostManager, ValidateCorrectProfile


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
    success_url = reverse_lazy('docapp:list_independent_employ')

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

# Process employ examination without company
def RegisterEmployExaminationWitoutExamination(request):
    pass

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

    def get(self, request, *args, **kwargs):
        labs = Laboratorio.objects.filter(is_active=True).count()
        if labs > 0:
            return super(RegisterEmployExamination, self).get(request, *args, **kwargs)
        else:
            messages.error(request, 'Por favor registre un laboratorio para poder iniciar procesos de examinacion')
            return redirect('docapp:dashboard')

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

    def get_queryset(self):
        if hasattr(self.request.user, 'doctor_profile'):
            return self.model.objects.exclude(manejador_por=self.request.user.doctor_profile)
        else:
            return super(ListExamination, self).get_queryset()


list_examination = ListExamination.as_view()


# End process examinations

# Process Laboratory
class RegisterLab(LoginRequiredMixin, CheckReceptionist, SuccessMessageMixin, CreateView):
    model = Laboratorio
    fields = ('nombre', 'direccion', 'email_contacto',)
    template_name = 'labapp/register/laboratory.html'
    success_url = reverse_lazy('docapp:list_lab')
    success_message = 'Laboratorio Registrado Existosamente'

    def form_valid(self, form):
        form.instance.registrado_por = self.request.user.reception_profile  # Add exclude field registrado_por
        return super(RegisterLab, self).form_valid(form=form)


register_lab = RegisterLab.as_view()


class UpdateLab(LoginRequiredMixin, CheckReceptionist, SuccessMessageMixin, UpdateView):
    pk_url_kwarg = 'lab_id'
    model = Laboratorio
    fields = ('nombre', 'direccion', 'email_contacto', 'is_active', )
    template_name = 'labapp/register/laboratory.html'
    success_url = reverse_lazy('docapp:list_lab')
    success_message = 'Laboratorio Actualizado Exitosamente'


update_lab = UpdateLab.as_view()


class DetailLab(LoginRequiredMixin, CheckReceptionist, DetailView):
    pk_url_kwarg = 'lab_id'
    model = Laboratorio
    context_object_name = 'lab'
    template_name = 'labapp/details/lab.html'


detail_laboratory = DetailLab.as_view()


class ListLab(LoginRequiredMixin, CheckReceptionist, SuccessMessageMixin, ListView):
    model = Laboratorio
    template_name = 'labapp/list/laboratory.html'


list_lab = ListLab.as_view()


class DeactivateLab(LoginRequiredMixin, CheckReceptionist, SingleObjectMixin, TemplateView):
    object = None
    pk_url_kwarg = 'lab_id'
    model = Laboratorio
    template_name = 'labapp/deactivate_object.html'
    redirect_url = reverse_lazy('docapp:list_lab')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        kwargs.update({'redirect_url': self.redirect_url})
        return super(DeactivateLab, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lab = self.get_object()
        lab.is_active = False
        try:
            lab.save()
        except IntegrityError:
            messages.error(message='Laboratorio No Desactivado', request=request)
        else:
            messages.success(message='Laboratorio Desactivado Exitosamente', request=request)
        return HttpResponseRedirect(reverse('docapp:list_lab'))


deactivate_lab = DeactivateLab.as_view()


class RegisterLabAdmin(LoginRequiredMixin, CheckReceptionist, SuccessMessageMixin, FormViewPutExtra):
    pk_url_kwarg = 'lab_id'
    form_class = BaseLabUserCreateForm
    model = User
    template_name = 'labapp/register/lab_user.html'
    success_url = reverse_lazy('docapp:list_lab')
    success_message = 'Administrador de laboratorio registrado existosamente'
    model_to_filter = Laboratorio

    def form_valid(self, form):
        lab = self.get_object()
        if form.is_valid():
            form.save(**{'is_admin': True, 'laboratorio_id': lab})
            return super(RegisterLabAdmin, self).form_valid(form=form)
        else:
            return super(RegisterLabAdmin, self).form_invalid(form=form)


register_lab_admin = RegisterLabAdmin.as_view()


class UpdateLabAdmin(LoginRequiredMixin, CheckReceptionist, ValidateCorrectProfile, SuccessMessageMixin, UpdateView):
    model = User
    form_class = BaseUserUpdateForm
    template_name = 'labapp/register/lab_user.html'
    success_url = reverse_lazy('docapp:list_lab')
    success_message = 'Administrador de laboratorio actualizado existosamente'
    profile_model = LaboratoryProfile
    profile_related_field = 'user_id'


update_lab_admin = UpdateLabAdmin.as_view()


class DeactivateLabAdmin(LoginRequiredMixin, CheckReceptionist, DeleteView):
    """ View to 'delete' doctor profile """
    context_object_name = 'instance'
    model = User
    template_name = 'accounts/delete_profile.html'
    success_url = reverse_lazy('docapp:list_lab')


deactivate_lab_admin = DeactivateLabAdmin.as_view()


class DetailLabAdmin(LoginRequiredMixin, CheckReceptionist, DetailView):
    context_object_name = 'instance'
    model = User
    template_name = 'accounts/show_profile.html'


detail_lab_admin = DetailLabAdmin.as_view()


class ListLabAdmin(LoginRequiredMixin, CheckReceptionist, SuccessMessageMixin, DetailView):
    model = Laboratorio
    template_name = 'labapp/list/admins.html'
    context_object_name = 'lab'

    def get_context_data(self, **kwargs):
        lab = self.get_object()
        kwargs.update({'admin_lab_list': lab.personal_lab.all().filter(is_admin=True)})
        return super(ListLabAdmin, self).get_context_data(**kwargs)


list_admin_lab = ListLabAdmin.as_view()


# End process laboratory


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
def make_consulta(request):
    try:
        if request.is_ajax():
            patient = PacienteParticular.objects.get(pk=int(request.POST.get('patiend_id')))
    except ObjectDoesNotExist:
        return Http404("El paciente no se encuentra registrado")
    else:
        Consulta(activated_by=request.user.reception_profile, paciente_id=patient).save()
        return HttpResponseRedirect(reverse_lazy('docapp:list_simple_patient'), status=200)


