from django.shortcuts import render, redirect, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.db import IntegrityError, transaction

from docapp.forms import CompanyForm, PersonForm, AntecedentForm, hazards_inlineformset, accidents_formset
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


class ListFilterView(ListView, SingleObjectMixin):
    """ Custom ListView to filter element only by pk_kwarg """
    model_to_filter = None
    context_object_2_name = None
    extra_context = None

    def get_object(self, queryset=None):
        """ Overwrite get_objet to only look with pk on Company model"""
        queryset = self.model_to_filter._default_manager.all()
        # Try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # If none of those are defined, it's an error.
        if pk is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(f"No {queryset.model._meta.verbose_name}s found matching the query")

        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Get context data from MultiObjectMixin and ContentMixin to replace SingleObjectMixin method """
        # Add custom SingleObject
        if self.context_object_2_name is not None:
            kwargs[self.context_object_2_name] = self.get_object()
        else:
            kwargs['simple_object'] = self.get_object()
        # MultipleObjectMixin
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            }
        if context_object_name is not None:
            context[context_object_name] = queryset

        context.update(kwargs)
        kwargs.update(context)  # Update kwargs with context information
        # ContentMixin section
        if 'view' not in kwargs:
            kwargs['view'] = self
        if self.extra_context:
            kwargs.update(self.extra_context)
        return kwargs


class FormViewPutExtra(FormView, SingleObjectMixin):
    model_to_filter = None
    context_object_2_name = 'parent_object'
    extra_context = None

    def get_object(self, queryset=None):
        """ Overwrite get_objet to get model_to_filter instance instead model instance """
        # get_objet to only look with pk on model_to_filter """
        queryset = self.model_to_filter._default_manager.all()
        # Try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # If none of those are defined, it's an error.
        if pk is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(f"No {queryset.model._meta.verbose_name}s found matching the query")

        return obj

    def get_context_data(self, **kwargs):
        """ Combine method from FormMixin and ContextMixin to manage correctly model """
        if self.context_object_2_name is not None:
            kwargs[self.context_object_2_name] = self.get_object()

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        if 'view' not in kwargs:
            kwargs['view'] = self
        if self.extra_context:
            kwargs.update(self.extra_context)

        return kwargs


class AntecedentPostManager(object):
    def post(self, request, *args, **kwargs):
        """ Overwrite post method to manage formsets """
        # Validate formsets
        hazard_formset = hazards_inlineformset(self.request.POST)
        accident_formset = accidents_formset(self.request.POST)

        if not hazard_formset.is_valid():
            messages.error(self.request, message="Error, Riesgos mal ingresados.")

        if not accident_formset.is_valid():
            messages.error(self.request, message="Error, Accidentes mal ingresados")

        if not hazard_formset.is_valid() or not accident_formset.is_valid():
            # Update formsets information (append errors and data)
            self.extra_context = {'accident_formset': accidents_formset,
                             'hazard_section': hazards_inlineformset}

            return self.form_invalid(form=self.get_form())

        antecedent_work = None
        if hasattr(self, '_custom_save'):
            """ Used only on Register Case """
            antecedent_work = self._custom_save(form=self.get_form())
            if not antecedent_work:
                # Update formsets information (append errors and data)
                self.extra_context = {'accident_formset': accidents_formset,
                                      'hazard_section': hazards_inlineformset}
                return self.form_invalid(form=self.get_form())
        
        response = super(AntecedentPostManager, self).post(request, *args, **kwargs)
        if antecedent_work is None:
            antecedent_work = self.object  # Is update process
        """ Managing formsets """
        # Get Hazard formset
        hazards = []
        for hazard in hazard_formset:
            data = {
                'fisico': hazard.cleaned_data.get('fisico'),
                'quimico': hazard.cleaned_data.get('quimico'),
                'mecanico': hazard.cleaned_data.get('mecanico'),
                'ergonomico': hazard.cleaned_data.get('ergonomico'),
                'electrico': hazard.cleaned_data.get('electrico'),
                'psicologico': hazard.cleaned_data.get('psicologico'),
                'work': antecedent_work,
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
        accidents = []
        for accident in accident_formset:
            data = {
                'secuelas': accident.cleaned_data.get('secuelas'),
                'tipo': accident.cleaned_data.get('tipo'),
                'atendido': accident.cleaned_data.get('atendido'),
                'calificado': accident.cleaned_data.get('calificado'),
                'fecha': accident.cleaned_data.get('fecha'),
                'description': accident.cleaned_data.get('description'),
                'work': antecedent_work,
                'create_by': self.request.user.reception_profile
            }
            accidents.append(JobAccidents(**data))

        try:
            with transaction.atomic():
                JobAccidents.objects.filter(work=antecedent_work).delete()
                JobAccidents.objects.bulk_create(accidents)
        except IntegrityError:
            messages.error(self.request, message='Error to save accidents')

        return response


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


class RegisterPerson(CheckReceptionist, LoginRequiredMixin, FormViewPutExtra):
    pk_url_kwarg = 'company_id'
    form_class = PersonForm
    model = Person
    template_name = 'docapp/register/register_simple_form.html'
    success_url = reverse_lazy('docapp:person_list')
    model_to_filter = Company
    extra_context = {'title': 'Registro empleado de la empresa '}

    def form_valid(self, form):
        company = self.get_object()
        form.company = company
        form.create_by = self.request.user.reception_profile
        instance = form.save()
        if instance:
            messages.success(self.request, message="Persona registrada exitosamente")
        return super(RegisterPerson, self).form_valid(form)


register_person = RegisterPerson.as_view()


class RegisterAntecedent(CheckReceptionist, LoginRequiredMixin, AntecedentPostManager, FormViewPutExtra):
    pk_url_kwarg = 'person_id'
    form_class = AntecedentForm
    model = AntecedentJobs
    template_name = 'docapp/register/register_antecedent_formsets.html'
    success_url = reverse_lazy('docapp:person_list')
    model_to_filter = Person
    context_object_2_name = 'person'
    extra_context = {'accident_formset': accidents_formset,
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
    template_name = 'docapp/register/register_simple_form.html'
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
    template_name = 'docapp/register/register_simple_form.html'
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


class UpdateAntecedent(CheckReceptionist, LoginRequiredMixin, AntecedentPostManager, UpdateView):
    pk_url_kwarg = 'antecedent_id'
    context_object_name = 'antecedent'
    model = AntecedentJobs
    form_class = AntecedentForm
    template_name = 'docapp/register/register_antecedent_formsets.html'
    success_url = reverse_lazy('docapp:person_list')

    def form_valid(self, form):
        """ Overwrite form_valid to add missing information"""
        antecedent = self.get_object()
        form.create_by = self.request.user.reception_profile
        form.person = antecedent.person
        return super(UpdateAntecedent, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """ Overwrite get_context_data method to append formset necessary"""
        antecedent = self.get_object()
        hazard_initial_data = [Hazards.objects.get(work=antecedent).as_dict()]
        accident_data = JobAccidents.objects.filter(work=antecedent)
        accident_initial_data = []
        for accident in accident_data:
            accident_initial_data.append(accident.as_dict())
        print(accident_initial_data)
        print(len(accident_initial_data))
        extra_context = {'hazard_section': hazards_inlineformset(initial=hazard_initial_data),
                         'accident_formset': accidents_formset(initial=accident_initial_data)}
        kwargs.update(extra_context)
        return super(UpdateAntecedent, self).get_context_data(**kwargs)


update_antecedent = UpdateAntecedent.as_view()


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


class DetailAntecedent(CheckReceptionist, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'antecedent_id'
    model = AntecedentJobs
    context_object_name = 'antecedent'
    template_name = 'docapp/details/antecedent.html'


detail_antecedent = DetailAntecedent.as_view()


def template_proof(request):
    return render(request, 'template_example.html')
