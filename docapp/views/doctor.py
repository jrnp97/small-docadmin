from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from docapp.models import Visiometry, ExamType
from docapp.forms import (VisioForm, sintomas_section, ant_enfermedad_section, ant_uso_lentes_section, ant_extra_exams,
                          agudeza_section, cronomatica_section)

from .chekers import CheckDoctor
from .customs import FormViewPutExtra, FormsetPostManager


class RegisterVisiometry(LoginRequiredMixin, CheckDoctor, FormsetPostManager, FormViewPutExtra):
    pk_url_kwarg = 'exam_id'
    model = Visiometry
    form_class = VisioForm
    model_to_filter = ExamType
    context_object_2_name = 'exam'
    extra_context = {'sintomas_section': sintomas_section,
                     'ant_enfermedad_section': ant_enfermedad_section,
                     'ant_uso_lentes_section': ant_uso_lentes_section,
                     'ant_extra_exams': ant_extra_exams,
                     'agudeza_section': agudeza_section,
                     'cronomatica_section': cronomatica_section}

    template_name = 'docapp/register/visiometry_formsets.html'
    success_url = reverse_lazy('docapp:exam_list')

    def _custom_save(self, form):
        exam_type = self.get_object()
        form.create_by = self.request.user.doctor_profile
        form.exam_type = exam_type
        instance = form.save()
        if instance:
            exam_type = exam_type.name
            messages.success(self.request, message=f"Examen de visiometria del proceso #{exam_type} "
                                                   f"registrado exitosamente")
        return instance


register_visiometry = RegisterVisiometry.as_view()
