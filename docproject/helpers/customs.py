from django.shortcuts import Http404, redirect
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.core.exceptions import SuspiciousOperation, ObjectDoesNotExist
from django.forms.models import BaseInlineFormSet
from django.core.urlresolvers import reverse_lazy
from django.db.models import ForeignKey

from docapp.models import Examinacion


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
        formsets_simple = {}
        formsets_with_files = {}

        for formset in self.extra_context.get('formsets'):
            """ Validating if value is a InlineFormSet and don't have initial data """
            value = formset.get('form')
            if formset.get('has_files'):
                formsets_with_files.update({formset.get('section_name'): value(self.request.POST, self.request.FILES)})
            else:
                formsets_simple.update({formset.get('section_name'): value(self.request.POST)})

        temp = []
        # Check simple formset
        for key, formset in formsets_simple.items():
            val = not formset.is_valid()
            if val:
                messages.error(self.request, message=f"Error, Guardando {key} datos mal ingresados")
            temp.append(val)

        # Check formset with files
        for key, formset in formsets_with_files.items():
            val = not formset.is_valid()
            if val:
                messages.error(self.request, message=f"Error, Guardando {key} datos mal ingresados")
            temp.append(val)

        # Check parent form
        val = not parent_form.is_valid()
        temp.append(val)
        if any(temp):
            # Update formsets information (append errors and data)
            return self.form_invalid(form=parent_form)

        object_parent = None
        if hasattr(self, '_custom_save'):
            """ Used only on Register Case """
            object_parent = self._custom_save(form=parent_form)
            if not object_parent:
                # Update formsets information (append errors and data)
                self.extra_context = formsets_simple.update(formsets_with_files)
                return self.form_invalid(form=parent_form)

        response = super(FormsetPostManager, self).post(request, *args, **kwargs)

        if object_parent is None:
            object_parent = self.object  # Is update process

        """ Managing simple formsets """
        parent_name = self.extra_context.get('parent_object_key')
        for formset in formsets_simple.values():
            temp = []
            delete_parent_name = None
            for form in formset:
                if len(form.cleaned_data) > 0:
                    form.cleaned_data.pop('DELETE', None)  # Clean formset data
                    data = form.cleaned_data.copy()
                    if data.get(parent_name):
                        data.update({parent_name: object_parent})
                        delete_parent_name = parent_name
                    if hasattr(formset.model, 'registrado_por'):
                        # Extract related name from relationship
                        alias = formset.model.registrado_por.field.related_model.user_id.field.related_query_name()
                        data.update({'registrado_por': getattr(self.request.user, alias)})
                    # Get other relationship fields on parent
                    fields = None or [field for field in formset.model._meta.local_fields if
                                      field.name in data.keys() and isinstance(field, ForeignKey) and data.get(
                                          field.name) is None]
                    if fields:
                        # Get parent information -- Assuming that all fields have the same parent
                        delete_parent_name = fields[0].name
                        object_parent = parent_form.cleaned_data.get(delete_parent_name)
                        for field in fields:  # Look value in parent_form
                            data.update({field.name: object_parent})

                    temp.append(formset.model(**data))
            try:
                with transaction.atomic():
                    if delete_parent_name:
                        formset.model.objects.filter(**{delete_parent_name: object_parent}).delete()
                    formset.model.objects.bulk_create(temp)
            except IntegrityError:
                messages.error(self.request, message="Error guardando informacion, revise")
                raise SuspiciousOperation(
                    "Error informacion Malformada"
                )

        """ Managins formsets with files """
        for formset in formsets_with_files.values():
            temp = []
            for form in formset:
                if len(form.cleaned_data) > 0:
                    data = form.cleaned_data.copy()
                    data.update({parent_name: object_parent})
                    if hasattr(formset.model, 'registrado_por'):
                        # Extract related name from relationship
                        alias = formset.model.create_by.field.related_model.user.field.cached_col.alias
                        data.update({'registrado_por': getattr(self.request.user, alias)})
                    temp.append(formset.model(**data))
                elif hasattr(form, 'instance'):
                    pass
            if len(temp) > 0:
                try:
                    with transaction.atomic():
                        formset.model.objects.filter(**{parent_name: object_parent}).delete()
                        formset.model.objects.bulk_create(temp)
                except IndentationError:
                    messages.error(self.request, message="Error guardando informacion")
                    raise SuspiciousOperation(
                        "Error informacion Malformada"
                    )

        return response


# Register exams
class BaseRegisterExamBehavior:
    pk_url_kwarg = 'exam_id'
    model_to_filter = Examinacion
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
            exam = Examinacion.objects.get(pk=exam_id)
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
    success_url = reverse_lazy('docapp:exam_list')

    def form_valid(self, form):
        """ Overwrite form_valid to add missing information"""
        object_saved = self.get_object()
        form.create_by = self.request.user.doctor_profile
        form.exam_type = object_saved.tipo_examen
        return super(BaseExamUpdateBehavior, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """ Overwrite to initialize form information putting initial data """
        kwargs.update({key: value for key, value in self.extra_context.items() if key != 'formsets'})
        actual_object = self.get_object()
        # Copy all formset to individuality
        section_names = []
        formsets = []
        titles = []
        for formset in self.extra_context.get('formsets'):
            # Validating if value is a InlineFormSet and don't have initial data
            value = formset.get('form')
            to_check = value.__class__ if value.__class__ != type else value
            if issubclass(to_check, BaseInlineFormSet) and value is to_check:
                formsets.append(formset.get('form'))
                section_names.append(formset.get('section_name'))
                titles.append(formset.get('title'))

        form_sets = {key: value for key, value in zip(section_names, formsets)}
        temp = None
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
            for idx, initial in enumerate(initial_data):
                formset_factory = formsets[idx]
                formsets[idx] = formset_factory(initial=initial)
            temp = []
            for title, section, form in zip(titles, section_names, formsets):
                temp.append({'title': title, 'section_name': section, 'form': form})
        if temp:
            kwargs.update({'formsets': temp})  # Update kwargs
        return super(BaseExamUpdateBehavior, self).get_context_data(**kwargs)
