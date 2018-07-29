from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.db import IntegrityError, transaction

from docapp.forms import CompanyForm, PersonForm, AntecedentForm, hazards_formset, accidents_formset
from docapp.models import Company, Person, AntecedentJobs, Hazards, JobAccidents


# Permissions checker
class CheckerBase(UserPassesTestMixin):
    def handle_no_permission(self):
        return redirect('docapp:dashboard')

    def test_func(self):
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
class CompanyList(CheckReceptionist, LoginRequiredMixin, ListView):
    context_object_name = 'company_list'
    model = Company
    template_name = 'docapp/lists/company_list.html'


company_list = CompanyList.as_view()


class PersonList(CheckReceptionist, LoginRequiredMixin, ListView):
    context_object_name = 'person_list'
    model = Person
    template_name = 'docapp/lists/person_list.html'


person_list = PersonList.as_view()


class AntecedentList(CheckReceptionist, LoginRequiredMixin, ListView, SingleObjectMixin):
    pk_url_kwarg = 'person_id'
    context_object_name = 'antecedent_list'
    model = AntecedentJobs
    template_name = 'docapp/lists/antecedent_list.html'

    def get_queryset(self):
        person = self.get_object()
        self.queryset = AntecedentJobs.objects.filter(person=person)
        return super(AntecedentList, self).get_queryset()

    def get_context_data(self, **kwargs):
        kwargs['person'] = self.get_object()
        return super(AntecedentList, self).get_context_data(**kwargs)


person_antecedent_list = AntecedentList.as_view()


# Register Views
class RegisterCompany(CheckReceptionist, LoginRequiredMixin, FormView):
    form_class = CompanyForm
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
        kwargs['detail'] = 'Empresas'
        return super(RegisterCompany, self).get_context_data(**kwargs)


register_company = RegisterCompany.as_view()


class RegisterPerson(CheckReceptionist, LoginRequiredMixin, FormView):
    form_class = PersonForm
    template_name = 'docapp/register/register_simple_form.html'
    success_url = reverse_lazy('docapp:register_person')

    def form_valid(self, form):
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona registrada exitosamente")
        return super(RegisterPerson, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['detail'] = 'Personas'
        return super(RegisterPerson, self).get_context_data(**kwargs)


register_person = RegisterPerson.as_view()


class RegisterAntecedent(CheckReceptionist, LoginRequiredMixin, FormView, SingleObjectMixin):
    pk_url_kwarg = 'person_id'
    form_class = AntecedentForm
    template_name = 'docapp/register/register_formsets.html'
    success_url = reverse_lazy('docapp:register_antecedent')

    def get_context_data(self, **kwargs):
        """ Overwriting get_context_data method to add formsets """
        kwargs['person'] = self.get_object()
        kwargs['accident_formset'] = accidents_formset
        kwargs['hazard_formset'] = hazards_formset
        return super(RegisterAntecedent, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.create_by = self.request.user.reception_profile
        form.person = self.request.person
        instance = form.save()
        if instance:
            person_name = self.request.person.get_full_name
            messages.success(self.request, message=f"Antecedente de {person_name} register exitosamente")
        return instance

    def post(self, request, *args, **kwargs):
        """ Overwrite post method to manage formsets """
        antecedent_work = super(RegisterAntecedent, self).post(request, *args, **kwargs)
        """ Managing formsets """
        # Hazard formset
        hazard_formset = hazards_formset(self.request.POST)
        hazards = []
        for hazard in hazard_formset:
            data = {
                'fisico': hazard.cleaned_data.get('fisico'),
                'quimico': hazard.cleaned_data.get('quimico'),
                'mecanico': hazard.cleaned_data.get('mecanico'),
                'ergonomico': hazard.cleaned_data.get('ergonomico'),
                'electrico': hazard.cleaned_data.get('electrico'),
                'psicologico': hazard.cleaned_data.get('psicologico'),
                'locativo': hazard.cleaned_data.get('locativo')
            }
            hazards.append(Hazards(**data))

        try:
            with transaction.atomic():
                Hazards.objects.filter(work=antecedent_work).delete()
                Hazards.objects.bulk_create(hazards)
        except IntegrityError:
            messages.error(self.request, message="Error to save riesgos")

        # Accident formset
        accident_formset = accidents_formset(self.request.POST)
        accidents = []
        for accident in accident_formset:
            data = {
                'secuelas': accident.cleaned_data.get('secuelas'),
                'tipo': accident.cleaned_data.get('tipo'),
                'atendido': accident.cleaned_data.get('atendido'),
                'calificado': accident.cleaned_data.get('calificado'),
                'fecha': accident.cleaned_data.get('fecha'),
                'description': accident.cleaned_data.get('description'),
                'create_by': self.request.user.reception_profile
            }
            accidents.append(JobAccidents(**data))

        try:
            with transaction.atomic():
                JobAccidents.objects.filter(work=antecedent_work).delete()
                JobAccidents.objects.bulk_create(accidents)
        except IntegrityError:
            messages.error(self.request, message='Error to save accidents')

        return antecedent_work


# Update Views
class UpdateCompany(CheckReceptionist, LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'company_id'
    context_object_name = 'company'
    model = Company
    form_class = CompanyForm
    template_name = 'docapp/register/register_simple_form.html'
    success_url = reverse_lazy('docapp:register_person')

    def form_valid(self, form):
        # Add Create_by
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Empresa actualizada existosamente")
        return super(UpdateCompany, self).form_valid(form)


update_company = UpdateCompany.as_view()


class UpdatePerson(CheckReceptionist, LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'person_id'
    context_object_name = 'person'
    model = Person
    form_class = PersonForm
    template_name = 'docapp/register/register_simple_form.html'
    success_url = reverse_lazy('docapp:register_person')

    def form_valid(self, form):
        # Add Create_by
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona actualizada existosamente")
        return super(UpdatePerson, self).form_valid(form)


update_person = UpdatePerson.as_view()


# Detail Views
class DetailCompany(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'company_id'
    model = Company
    context_object_name = 'company'
    template_name = 'docapp/details/company.html'


detail_company = DetailCompany.as_view()


class DetailPerson(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'person_id'
    model = Person
    context_object_name = 'person'
    template_name = 'docapp/details/person.html'


detail_person = DetailPerson.as_view()
