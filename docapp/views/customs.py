from django.shortcuts import Http404
from django.views.generic import ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.core.exceptions import SuspiciousOperation
from django.forms.models import BaseInlineFormSet

from docapp.models import Hazards, JobAccidents
from docapp.forms import (hazards_inlineformset, accidents_formset, )


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


class FormsetPostManager(object):
    def post(self, request, *args, **kwargs):
        """ Overwrite post method to manage formset """
        form_sets = {}
        for key, value in self.extra_context.items():
            print(f"{key} = {value}")
            if issubclass(value.__class__, BaseInlineFormSet):
                form_sets.update({key: value(self.request.POST)})

        temp = []
        for key, formset in form_sets.items():
            val = not formset.is_valid()
        if val:
            messages.error(self.request, message=f"Error, Guardando {key} data mal ingresada")
        temp.append(val)

        if any(temp):
            # Update formsets information (append errors and data)
            self.extra_context = form_sets.copy()
        return self.form_invalid(form=self.get_form())


        object_parent = None
        if hasattr(self, '_custom_save'):
            """ Used only on Register Case """
            object_parent = self._custom_save(form=self.get_form())
            if not object_parent:
                # Update formsets information (append errors and data)
                self.extra_context = form_sets.copy()
                return self.form_invalid(form=self.get_form())

        response = super(FormsetPostManager, self).post(request, *args, **kwargs)

        if object_parent is None:
            object_parent = self.object  # Is update process

        """ Managing formsets """
        for formset in form_sets.values():
            temp = []
            for form in formset:
                data = form.cleaned_data.copy()
                data.update({'vision': object_parent})
                temp.append(formset.model(**data))
            try:
                with transaction.atomic():
                    formset.model.objects.filter(**{kwargs.pop('parent_object_key', None): object_parent}).delete()
                    formset.model.objects.bulk_create(temp)
            except IntegrityError:
                object_parent.delete()
                messages.error(self.request, message="Error guardando informacion, revise")
                raise SuspiciousOperation(message='Error Informacion Erronea')

        return response
