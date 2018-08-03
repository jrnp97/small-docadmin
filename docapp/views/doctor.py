from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from docapp.models import Visiometry, Audiology, Audiometry
from docapp.forms import (VisioForm, sintomas_section, ant_enfermedad_section, ant_uso_lentes_section, ant_extra_exams,
                          agudeza_section, cronomatica_section,
                          AudioForm, ananmesis_section, ant_familiar_section, ant_otro_section, exposicion_section,
                          estado_actual_section,
                          AudiometriaForm, otoscopia_section, information_section)

from .chekers import CheckDoctor
from .customs import FormViewPutExtra, FormsetPostManager, BaseRegisterExamBehavior, BaseExamUpdateBehavior


# Register views
class RegisterVisiometry(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                         FormViewPutExtra):
    model = Visiometry
    form_class = VisioForm
    extra_context = {'exam_name': 'visiometria',
                     'parent_object_key': 'visiometry',
                     'sintomas_section': sintomas_section,
                     'ant_enfermedad_section': ant_enfermedad_section,
                     'ant_uso_lentes_section': ant_uso_lentes_section,
                     'ant_extra_exams': ant_extra_exams,
                     'agudeza_section': agudeza_section,
                     'cronomatica_section': cronomatica_section
                     }

    template_name = 'docapp/register/visiometry_formsets.html'


register_visiometry = RegisterVisiometry.as_view()


class RegisterAudiology(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                         FormViewPutExtra):
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


class RegisterAudiometry(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                         FormViewPutExtra):
    model = Audiometry
    form_class = AudiometriaForm
    extra_context = {'exam_name': 'audiometria',
                     'parent_object_key': 'audiometry',
                     'otoscopia_section': otoscopia_section,
                     'information_section': information_section
                     }
    template_name = 'docapp/register/audiometry_formsets.html'


register_audiometry = RegisterAudiometry.as_view()


# Update views
class UpdateVisiometry(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Visiometry
    form_class = VisioForm
    template_name = 'docapp/register/visiometry_formsets.html'
    extra_context = {'exam_name': 'visiometria',
                     'parent_object_key': 'visiometry',
                     'sintomas_section': sintomas_section,
                     'ant_enfermedad_section': ant_enfermedad_section,
                     'ant_uso_lentes_section': ant_uso_lentes_section,
                     'ant_extra_exams': ant_extra_exams,
                     'agudeza_section': agudeza_section,
                     'cronomatica_section': cronomatica_section
                     }


update_visiometry = UpdateVisiometry.as_view()


class UpdateAudiology(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
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


update_audiology = UpdateAudiology.as_view()


class UpdateAudiometry(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Audiometry
    form_class = AudiometriaForm
    extra_context = {'exam_name': 'audiometria',
                     'parent_object_key': 'audiometry',
                     'otoscopia_section': otoscopia_section,
                     'information_section': information_section
                     }
    template_name = 'docapp/register/audiometry_formsets.html'


update_audiometry = UpdateAudiometry.as_view()
