from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy
"""
from docapp.models import Visiometry, Audiology, Audiometry, Occupational, ExamType
from docapp.forms import (VisioForm, sintomas_section, ant_enfermedad_section, ant_uso_lentes_section, ant_extra_exams,
                          agudeza_section, cronomatica_section,
                          AudioForm, ananmesis_section, ant_familiar_section, ant_otro_section, exposicion_section,
                          estado_actual_section,
                          AudiometriaForm, otoscopia_section, information_section,
                          OcupaForm, ant_familiares_section, habitos_section, fisico_general_form,
                          organos_sentidos_section, conclusion_section,
                          ExamForm)

from .chekers import CheckDoctor
from .customs import FormViewPutExtra, FormsetPostManager, BaseRegisterExamBehavior, BaseExamUpdateBehavior


# Register views
class RegisterVisiometry(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                         FormViewPutExtra):
    model = Visiometry
    form_class = VisioForm
    template_name = 'docapp/register/exam_register.html'
    extra_context = {'exam_name': 'visiometria',
                     'parent_object_key': 'visiometry',
                     'formsets': [
                         {'section_name': 'sintomas',
                          'title': 'Sintomas',
                          'form': sintomas_section},

                         {'section_name': 'ant_enfermedad',
                          'title': 'Antecedentes de Enfermedades',
                          'form': ant_enfermedad_section},

                         {'section_name': 'ant_uso_lentes',
                          'title': 'Antecedentes de Uso de Lentes',
                          'form': ant_uso_lentes_section},

                         {'section_name': 'ant_extra_exams',
                          'title': 'Antecedentes de Examanes',
                          'form': ant_extra_exams},

                         {'section_name': 'agudeza',
                          'title': 'Agudeza',
                          'form': agudeza_section},

                         {'section_name': 'cronomatica',
                          'title': 'Cronomatica',
                          'form': cronomatica_section}
                     ]
                     }


register_visiometry = RegisterVisiometry.as_view()


class RegisterAudiology(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                        FormViewPutExtra):
    model = Audiology
    form_class = AudioForm
    template_name = 'docapp/register/exam_register.html'
    extra_context = {'exam_name': 'audiologia',
                     'parent_object_key': 'audiology',
                     'formsets': [
                         {'section_name': 'ananmesis',
                          'title': 'Ananmesis',
                          'form': ananmesis_section},

                         {'section_name': 'ant_familiar',
                          'title': 'Antecedentes Familiares',
                          'form': ant_familiar_section},

                         {'section_name': 'ant_otros',
                          'title': 'Otros Antecedentes',
                          'form': ant_otro_section},

                         {'section_name': 'exposicion',
                          'title': 'Exposiciones',
                          'form': exposicion_section},

                         {'section_name': 'estado_actual',
                          'title': 'Estado Actual',
                          'form': estado_actual_section},
                     ]
                     }


register_audiology = RegisterAudiology.as_view()


class RegisterAudiometry(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                         FormViewPutExtra):
    model = Audiometry
    form_class = AudiometriaForm
    template_name = 'docapp/register/exam_register.html'
    extra_context = {'exam_name': 'audiometria',
                     'parent_object_key': 'audiometry',
                     'formsets': [
                         {'section_name': 'otoscopia',
                          'title': 'Otoscopia',
                          'form': otoscopia_section},
                         {'section_name': 'information',
                          'title': 'Información',
                          'form': information_section}
                     ]
                     }


register_audiometry = RegisterAudiometry.as_view()


class RegisterOccupational(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                           FormViewPutExtra):
    model = Occupational
    form_class = OcupaForm
    template_name = 'docapp/register/exam_register.html'
    extra_context = {'exam_name': 'ocupacional',
                     'parent_object_key': 'occupational',
                     'formsets': [
                         {'section_name': 'ant_familiares',
                          'title': 'Antecedentes Familiares',
                          'form': ant_familiares_section},

                         {'section_name': 'habitos',
                          'title': 'Habitos',
                          'form': habitos_section},

                         {'section_name': 'fisico_general',
                          'title': 'Estado Fisico General',
                          'form': fisico_general_form},

                         {'section_name': 'organos_sentidos',
                          'title': 'Organos de los Sentidos',
                          'form': organos_sentidos_section},

                         {'section_name': 'conclusion',
                          'title': 'Conclusiones',
                          'form': conclusion_section}
                     ]
                     }


register_occupational = RegisterOccupational.as_view()


# Update views
class UpdateVisiometry(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Visiometry
    form_class = VisioForm
    template_name = 'docapp/register/exam_register.html'
    extra_context = {'exam_name': 'visiometria',
                     'parent_object_key': 'visiometry',
                     'formsets': [
                         {'section_name': 'sintomas',
                          'title': 'Sintomas',
                          'form': sintomas_section},

                         {'section_name': 'ant_enfermedad',
                          'title': 'Antecedentes de Enfermedades',
                          'form': ant_enfermedad_section},

                         {'section_name': 'ant_uso_lentes',
                          'title': 'Antecedentes de Uso de Lentes',
                          'form': ant_uso_lentes_section},

                         {'section_name': 'ant_extra_exams',
                          'title': 'Antecedentes de Examanes',
                          'form': ant_extra_exams},

                         {'section_name': 'agudeza',
                          'title': 'Agudeza',
                          'form': agudeza_section},

                         {'section_name': 'cronomatica',
                          'title': 'Cronomatica',
                          'form': cronomatica_section}
                     ]
                     }


update_visiometry = UpdateVisiometry.as_view()


class UpdateAudiology(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Audiology
    form_class = AudioForm
    template_name = 'docapp/register/exam_register.html'
    extra_context = {'exam_name': 'audiologia',
                     'parent_object_key': 'audiology',
                     'formsets': [
                         {'section_name': 'ananmesis',
                          'title': 'Ananmesis',
                          'form': ananmesis_section},

                         {'section_name': 'ant_familiar',
                          'title': 'Antecedentes Familiares',
                          'form': ant_familiar_section},

                         {'section_name': 'ant_otros',
                          'title': 'Otros Antecedentes',
                          'form': ant_otro_section},

                         {'section_name': 'exposicion',
                          'title': 'Exposiciones',
                          'form': exposicion_section},

                         {'section_name': 'estado_actual',
                          'title': 'Estado Actual',
                          'form': estado_actual_section},
                     ]
                     }


update_audiology = UpdateAudiology.as_view()


class UpdateAudiometry(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Audiometry
    form_class = AudiometriaForm
    template_name = 'docapp/register/exam_register.html'
    extra_context = {'exam_name': 'audiometria',
                     'parent_object_key': 'audiometry',
                     'formsets': [
                         {'section_name': 'otoscopia',
                          'title': 'Otoscopia',
                          'form': otoscopia_section},
                         {'section_name': 'information',
                          'title': 'Información',
                          'form': information_section}
                     ]
                     }


update_audiometry = UpdateAudiometry.as_view()


class UpdateOccupational(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Occupational
    form_class = OcupaForm
    template_name = 'docapp/register/exam_register.html'
    extra_context = {'exam_name': 'ocupacional',
                     'parent_object_key': 'occupational',
                     'formsets': [
                         {'section_name': 'ant_familiares',
                          'title': 'Antecedentes Familiares',
                          'form': ant_familiares_section},

                         {'section_name': 'habitos',
                          'title': 'Habitos',
                          'form': habitos_section},

                         {'section_name': 'fisico_general',
                          'title': 'Estado Fisico General',
                          'form': fisico_general_form},

                         {'section_name': 'organos_sentidos',
                          'title': 'Organos de los Sentidos',
                          'form': organos_sentidos_section},

                         {'section_name': 'conclusion',
                          'title': 'Conclusiones',
                          'form': conclusion_section}
                     ]
                     }


update_occupational = UpdateOccupational.as_view()

"""