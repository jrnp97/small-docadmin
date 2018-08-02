from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from docapp.models import ExamType, Visiometry, Audiology
from docapp.forms import (VisioForm, sintomas_section, ant_enfermedad_section, ant_uso_lentes_section, ant_extra_exams,
                          agudeza_section, cronomatica_section,
                          AudioForm, ananmesis_section, ant_familiar_section, ant_otro_section, exposicion_section,
                          estado_actual_section)

from .chekers import CheckDoctor
from .customs import FormViewPutExtra, FormsetPostManager


class BaseRegisterView(LoginRequiredMixin, CheckDoctor, FormsetPostManager, FormViewPutExtra):
    pk_url_kwarg = 'exam_id'
    model_to_filter = ExamType
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


class RegisterVisiometry(BaseRegisterView):
    model = Visiometry
    form_class = VisioForm
    extra_context = {'exam_name': 'visiometria',
                     'parent_object_key': 'vision',
                     'sintomas_section': sintomas_section,
                     'ant_enfermedad_section': ant_enfermedad_section,
                     'ant_uso_lentes_section': ant_uso_lentes_section,
                     'ant_extra_exams': ant_extra_exams,
                     'agudeza_section': agudeza_section,
                     'cronomatica_section': cronomatica_section}

    template_name = 'docapp/register/visiometry_formsets.html'


register_visiometry = RegisterVisiometry.as_view()


class RegisterAudiology(BaseRegisterView):
    model = Audiology
    form_class = AudioForm
    extra_context = {'exam_name': 'audiologia',
                     'parent_object_key': 'audiology',
                     'ananmesis_section': ananmesis_section,
                     'ant_familiar_section': ant_familiar_section,
                     'ant_otro_section': ant_otro_section,
                     'exposicion_section': exposicion_section,
                     'estado_actual_section': estado_actual_section,
                     }

    template_name = 'docapp/register/audiology_formsets.html'


register_audiology = RegisterAudiology.as_view()
