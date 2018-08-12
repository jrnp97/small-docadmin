from django.shortcuts import Http404, redirect
from django.views.generic import ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.core.exceptions import SuspiciousOperation, ObjectDoesNotExist
from django.forms.models import BaseInlineFormSet
from django.core.urlresolvers import reverse_lazy

from docapp.models import TipoExamen


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


class FormsetPostManager(object):
    def post(self, request, *args, **kwargs):
        """ Overwrite post method to manage formset """
        parent_form = self.get_form()
        form_sets = {}

        for formset in self.extra_context.get('formsets'):
            """ Validating if value is a InlineFormSet and don't have initial data """
            value = formset.get('form')
            to_check = value.__class__ if value.__class__ != type else value
            if issubclass(to_check, BaseInlineFormSet) and value is to_check:
                form_sets.update({formset.get('section_name'): value(self.request.POST, self.request.FILES)})
                # TODO Make a constraint to only put request.FILES to formset must have

        temp = []
        for key, formset in form_sets.items():
            val = not formset.is_valid()
            if val:
                messages.error(self.request, message=f"Error, Guardando {key} datos mal ingresados")
            temp.append(val)

        if any(temp):
            # Update formsets information (append errors and data)
            for key, value in form_sets.items():
                pos = -1
                for idx, formset in enumerate(self.extra_context['formsets']):
                    if formset['section_name'] == key:
                        pos = idx
                        break
                else:
                    raise SuspiciousOperation(
                        "Error en intern process"
                    )
                self.extra_context['formsets'][pos]['form'] = value
            return self.form_invalid(form=parent_form)
            # TODO Check if form_invalid method work with self.object when is None

        object_parent = None
        if hasattr(self, '_custom_save'):
            """ Used only on Register Case """
            object_parent = self._custom_save(form=parent_form)
            if not object_parent:
                # Update formsets information (append errors and data)
                self.extra_context = form_sets.copy()
                return self.form_invalid(form=parent_form)

        response = super(FormsetPostManager, self).post(request, *args, **kwargs)

        if object_parent is None:
            object_parent = self.object  # Is update process

        """ Managing formsets """
        parent_name = self.extra_context.get('parent_object_key')
        for formset in form_sets.values():
            temp = []
            for form in formset:
                if len(form.cleaned_data) > 0:
                    form.cleaned_data.pop('DELETE', None)  # Clean formset data
                    data = form.cleaned_data.copy()
                    data.update({parent_name: object_parent})
                    if hasattr(formset.model, 'create_by'):
                        # Extract related name from relationship
                        alias = formset.model.create_by.field.related_model.user.field.cached_col.alias
                        data.update({'create_by': getattr(self.request.user, alias)})
                    temp.append(formset.model(**data))
            try:
                with transaction.atomic():
                    formset.model.objects.filter(**{parent_name: object_parent}).delete()
                    formset.model.objects.bulk_create(temp)
            except IntegrityError:
                messages.error(self.request, message="Error guardando informacion, revise")
                raise SuspiciousOperation(message='Error Informacion Erronea')

        return response


# Register exams
class BaseRegisterExamBehavior:
    pk_url_kwarg = 'exam_id'
    model_to_filter = TipoExamen
    context_object_2_name = 'exam'
    success_url = reverse_lazy('docapp:exam_list')

    def _custom_save(self, form):
        exam_type = self.get_object()
        form.create_by = self.request.user.doctor_profile
        form.exam_type = exam_type
        instance = form.save()
        if instance:
            messages.success(self.request, message=f"Examen de {self.extra_context.get('exam_name')}"
                                                   f" del proceso #{exam_type.id} "
                                                   f"registrado exitosamente")
        return instance

    def get(self, request, *args, **kwargs):
        exam_id = kwargs.get('exam_id')
        try:
            exam = TipoExamen.objects.get(pk=exam_id)
        except ObjectDoesNotExist:
            pass
        else:
            child_name = self.extra_context.get('parent_object_key')
            if hasattr(exam, child_name):
                messages.info(request,
                              message=f"Los resultados de {self.extra_context.get('exam_name')} estan registrados"
                                      f", actualice si desea")
                child_exam = getattr(exam, child_name)
                return redirect('docapp:update_%s' % child_name, pk=child_exam.id)

        return super(BaseRegisterExamBehavior, self).get(request, *args, **kwargs)


# Update exams
class BaseExamUpdateBehavior:
    success_url = reverse_lazy('docapp:person_list')
    extra_content = None

    def form_valid(self, form):
        """ Overwrite form_valid to add missing information"""
        object_saved = self.get_object()
        form.create_by = self.request.user.reception_profile
        form.exam_type = object_saved.exam_type
        return super(BaseExamUpdateBehavior, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """ Overwrite to initialize form information putting initial data """
        actual_object = self.get_object()
        form_sets = {}

        for formset in self.extra_context.get('formsets'):
            """ Validating if value is a InlineFormSet and don't have initial data """
            value = formset.get('form')
            to_check = value.__class__ if value.__class__ != type else value
            if issubclass(to_check, BaseInlineFormSet) and value is to_check:
                form_sets.update({formset.get('section_name'): value})

        if len(form_sets) > 0:
            # Get initial data
            alias = self.extra_context.get('parent_object_key')

            initial_data = []

            for formset in form_sets.values():
                try:
                    data = formset.model.objects.get(**{alias: actual_object})
                except ObjectDoesNotExist:
                    initial_data.append([])
                else:
                    dict_data = vars(data)
                    # Delete unneeded info
                    dict_data.pop('_state', None)
                    dict_data.pop('id', None)
                    initial_data.append([dict_data])
            # put data on extra_content
            for key, initial in zip(form_sets.keys(), initial_data):
                post = 0
                for idx, formset_dict in enumerate(self.extra_context['formsets']):
                    if formset_dict.get('section_name') == key:
                        post = idx
                        break
                else:
                    raise ValueError("Error formset information")

                formset_factory =  self.extra_context['formsets'][post].get('form')
                self.extra_context['formsets'][post]['form'] = formset_factory(initial=initial)

        kwargs.update(self.extra_context)  # Update kwargs
        return super(BaseExamUpdateBehavior, self).get_context_data(**kwargs)
