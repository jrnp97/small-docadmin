from django.shortcuts import redirect



"""from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy


class RegisterLaboratory(LoginRequiredMixin, CheckLaboratory, BaseRegisterExamBehavior, FormsetPostManager,
                         FormViewPutExtra):
    model = Laboratory
    form_class = LabForm
    template_name = 'docapp/register/exams/laboratory.html'
    extra_context = {'exam_name': 'laboratorio',
                     'parent_object_key': 'laboratory',
                     'formsets': [
                         {'section_name': 'blood',
                          'title': 'Examen de Sangre',
                          'form': blood_section},
                         {'section_name': 'exams',
                          'title': 'Examenes',
                          'form': exams_section}
                     ]
                     }

    def _custom_save(self, form):
        exam_type = self.get_object()
        form.create_by = self.request.user.laboratory_profile
        form.exam_type = exam_type
        instance = form.save()
        if instance:
            messages.success(self.request, message=f"Examen de {self.extra_context.get('exam_name')}"
                                                   f" del proceso #{exam_type.id} "
                                                   f"registrado exitosamente")
        return instance


register_laboratory = RegisterLaboratory.as_view()


class UpdateLaboratory(LoginRequiredMixin, CheckLaboratory, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Laboratory
    form_class = LabForm
    success_url = reverse_lazy('docapp:exam_list')
    extra_context = {'exam_name': 'laboratorio',
                     'parent_object_key': 'laboratory',
                     'formsets': [
                         {'section_name': 'blood',
                          'title': 'Examen de Sangre',
                          'form': blood_section},
                         {'section_name': 'exams',
                          'title': 'Examenes',
                          'form': exams_section}
                     ]
                     }
    template_name = 'docapp/register/exam_register.html'

    def form_valid(self, form):
        # Overwrite form_valid to add missing information
        object_saved = self.get_object()
        form.create_by = self.request.user.laboratory_profile
        form.exam_type = object_saved.exam_type
        return super(BaseExamUpdateBehavior, self).form_valid(form)


update_laboratory = UpdateLaboratory.as_view()
"""