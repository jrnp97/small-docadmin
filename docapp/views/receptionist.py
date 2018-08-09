from django.shortcuts import redirect
from django.views.generic import FormView, ListView, UpdateView, DetailView, TemplateView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from docapp.forms import CompanyForm, PersonForm, AntecedentForm, hazards_inlineformset, accidents_formset, ExamForm
from docapp.models import Company, Person, AntecedentJobs, Hazards, JobAccidents, ExamType

from .chekers import CheckReceptionist, CheckUser, CheckRecOrDoc
from .customs import ListFilterView, FormViewPutExtra, FormsetPostManager


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


class PersonListFilter(CheckReceptionist, LoginRequiredMixin, ListFilterView):
    pk_url_kwarg = 'company_id'
    context_object_name = 'person_list'
    model = Person
    model_to_filter = Company
    context_object_2_name = 'company'
    template_name = 'docapp/lists/person_list_company.html'

    def get_queryset(self):
        company = self.get_object()
        self.queryset = Person.objects.filter(company=company)
        return super(PersonListFilter, self).get_queryset()


filter_person_list = PersonListFilter.as_view()


class AntecedentList(CheckReceptionist, LoginRequiredMixin, ListFilterView):
    pk_url_kwarg = 'person_id'
    context_object_name = 'antecedent_list'
    model = AntecedentJobs
    model_to_filter = Person
    context_object_2_name = 'person'
    template_name = 'docapp/lists/antecedent_list.html'

    def get_queryset(self):
        person = self.get_object()
        self.queryset = AntecedentJobs.objects.filter(person=person)
        return super(AntecedentList, self).get_queryset()


person_antecedent_list = AntecedentList.as_view()


# Register Views
class RegisterCompany(CheckReceptionist, LoginRequiredMixin, FormView):
    form_class = CompanyForm
    template_name = 'docapp/register/company.html'
    success_url = reverse_lazy('docapp:company_list')

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


class RegisterPerson(CheckReceptionist, LoginRequiredMixin, FormViewPutExtra):
    pk_url_kwarg = 'company_id'
    form_class = PersonForm
    model = Person
    template_name = 'docapp/register/employ.html'
    success_url = reverse_lazy('docapp:person_list')
    model_to_filter = Company

    def form_valid(self, form):
        company = self.get_object()
        form.company = company
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona registrada exitosamente")
        return super(RegisterPerson, self).form_valid(form)


register_person = RegisterPerson.as_view()


class RegisterAntecedent(CheckReceptionist, LoginRequiredMixin, FormsetPostManager, FormViewPutExtra):
    pk_url_kwarg = 'person_id'
    form_class = AntecedentForm
    model = AntecedentJobs
    template_name = 'docapp/register/register_antecedent_formsets.html'
    success_url = reverse_lazy('docapp:person_list')
    model_to_filter = Person
    context_object_2_name = 'person'
    extra_context = {'parent_object_key': 'work',
                     'accident_formset': accidents_formset,
                     'hazard_section': hazards_inlineformset}

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
class UpdateCompany(CheckReceptionist, LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'company_id'
    context_object_name = 'company'
    model = Company
    form_class = CompanyForm
    template_name = 'docapp/register/company.html'
    success_url = reverse_lazy('docapp:company_list')

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
    model = AntecedentJobs
    form_class = AntecedentForm
    template_name = 'docapp/register/register_antecedent_formsets.html'
    success_url = reverse_lazy('docapp:person_list')
    extra_context = {'parent_object_key': 'work',
                     'accident_formset': accidents_formset,
                     'hazard_section': hazards_inlineformset}

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
            hazard_initial_data = [Hazards.objects.get(work=antecedent).as_dict()]
        except ObjectDoesNotExist:
            hazard_initial_data = []
        accident_data = JobAccidents.objects.filter(work=antecedent)
        accident_initial_data = []
        for accident in accident_data:
            accident_initial_data.append(accident.as_dict())
        print(accident_initial_data)
        print(len(accident_initial_data))
        self.extra_context = {'parent_object_key': 'work',
                              'hazard_section': hazards_inlineformset(initial=hazard_initial_data),
                              'accident_formset': accidents_formset(initial=accident_initial_data)}
        kwargs.update(self.extra_context)
        return super(UpdateAntecedent, self).get_context_data(**kwargs)


update_antecedent = UpdateAntecedent.as_view()


# Detail Views
class DetailCompany(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'company_id'
    model = Company
    context_object_name = 'company'
    template_name = 'docapp/details/company.html'


detail_company = DetailCompany.as_view()


class DetailPerson(CheckRecOrDoc, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'person_id'
    model = Person
    context_object_name = 'person'
    template_name = 'docapp/details/person.html'


detail_person = DetailPerson.as_view()


class DetailAntecedent(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'antecedent_id'
    model = AntecedentJobs
    context_object_name = 'antecedent'
    template_name = 'docapp/details/antecedent.html'


detail_antecedent = DetailAntecedent.as_view()


class RegisterExam(CheckReceptionist, LoginRequiredMixin, FormViewPutExtra):
    pk_url_kwarg = 'person_id'
    model = ExamType
    form_class = ExamForm
    model_to_filter = Person
    context_object_2_name = 'person'
    success_url = reverse_lazy('docapp:dashboard')
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
    model = ExamType
    context_object_name = 'exam_list'
    template_name = 'docapp/lists/exam_list.html'


exam_list = ExamList.as_view()
