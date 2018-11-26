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
            if kwargs.get('extra_context') is None:
                kwargs.update(self.extra_context)
            else:
                extra = kwargs.pop('extra_context')
                kwargs.update(extra)

        return kwargs


class FormsetPostManager(object):
    def post(self, request, *args, **kwargs):
        """ Overwrite post method to manage formset """
        parent_form = self.get_form()
        formsets_simple = {}
        formsets = self.extra_context.copy()
        temp = []
        # Check parent form
        val = not parent_form.is_valid()
        temp.append(val)
        for element in formsets.get('formsets'):
            """ Validating formsets """
            if element:
                formset = element.get('form')
                section_name = element.get('title')
                if element.get('has_files'):
                    formset = formset(self.request.POST,
                                      self.request.FILES) if formset.__class__ is type else formset.__class__(
                        self.request.POST, self.request.FILES)
                else:
                    formset = formset(self.request.POST) if formset.__class__ is type else formset.__class__(
                        self.request.POST)
                formsets_simple.update({section_name: formset})
                val = not formset.is_valid()
                temp.append(val)
                if val:
                    messages.error(self.request, message=f"Error, Guardando {section_name} datos mal ingresados")
                element.update({'form': formset})

        if any(temp):
            return self.render_to_response(self.get_context_data(form=parent_form, extra_context=formsets))

        object_parent = None
        if hasattr(self, '_custom_save'):
            """ Used only on Register Case """
            object_parent = self._custom_save(form=parent_form)
            if not object_parent:
                return self.form_invalid(form=parent_form, extra_context=formsets)

        response = super(FormsetPostManager, self).post(request, *args, **kwargs)

        if object_parent is None:
            object_parent = self.object  # Is update process

        """ Managing simple formsets """
        parent_name = self.extra_context.get('parent_object_key')
        for formset in formsets_simple.values():
            temp = []
            delete_parent_name = None
            for form in formset:
                if form.cleaned_data:
                    if not form.cleaned_data.pop('DELETE', None):
                        data = form.cleaned_data.copy()
                        if data.get(parent_name):
                            data.update({parent_name: object_parent})
                            delete_parent_name = parent_name
                        if hasattr(formset.model, 'registrado_por'):
                            # Extract related name from relationship
                            alias = formset.model.registrado_por.field.related_model.user_id.field.related_query_name()
                            data.update({'registrado_por': getattr(self.request.user, alias)})
                        # Get all parent relations required on formset
                        # parent_fields = set([field.name for field in object_parent._meta.get_fields()])
                        parent_fields = set(parent_form.cleaned_data.keys())
                        form_fields = set([field.name for field in formset.model._meta.get_fields()])
                        # Clean id's
                        try:
                            form_fields.remove('id')
                        except KeyError:
                            pass

                        try:
                            parent_fields.remove('id')
                        except KeyError:
                            pass

                        fields = form_fields.intersection(parent_fields) or None
                        if fields:
                            for field in iter(fields):
                                # Set value of field and insert to data suppose that field is a relationship
                                data.update({field: parent_form.cleaned_data.get(field).first()})
                        temp.append(formset.model(**data))

            if temp:
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

        return response


# Register exams
class BaseRegisterExamBehavior:
    pk_url_kwarg = 'exam_id'
    model_to_filter = Examinacion
    context_object_2_name = 'exam'
    success_url = reverse_lazy('docapp:doctor_own_examinations')

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
            child_name = self.extra_context.get('child_name')
            if hasattr(exam, child_name):
                messages.info(request,
                              message=f"Los resultados de {self.extra_context.get('exam_name')} estan registrados"
                                      f", actualice si desea")
                child_exam = getattr(exam, child_name)
                return redirect('docapp:update_%s' % child_name, pk=child_exam.id)

        return super(BaseRegisterExamBehavior, self).get(request, *args, **kwargs)


# Update exams
class BaseExamUpdateBehavior:
    success_url = reverse_lazy('docapp:doctor_own_examinations')

    def form_valid(self, form):
        """ Overwrite form_valid to add missing information"""
        object_saved = self.get_object()
        form.create_by = self.request.user.doctor_profile
        form.exam_type = object_saved.examinacion_id
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


# Validate Correct Profile
class ValidateCorrectProfile(SingleObjectMixin):
    """ Class to validate if a user consult have profile specify """
    profile_model = None
    profile_related_field = None

    def get_object(self, queryset=None):
        assert self.profile_model and self.profile_related_field, ValueError(
            "Error specify profile_model and profile_related_model")
        obj = super(ValidateCorrectProfile, self).get_object(queryset=queryset)
        try:
            self.profile_model.objects.get(**{self.profile_related_field: obj})
        except ObjectDoesNotExist:
            raise SuspiciousOperation("You are trying do something bad")
        else:
            return obj
