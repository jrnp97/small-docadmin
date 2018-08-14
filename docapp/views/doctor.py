from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy

from docapp.models import TipoExamen, Occupational, Audiology
from docapp.forms import (OcupaForm,
                          ant_familiares_section,
                          ant_gineco_section,
                          habito_alcohol_section, habito_cigarillo_section, habito_droga_section,
                          habito_general_section,
                          examen_fisico_general_section,
                          examen_fisico_ojos_section, examen_fisico_oidos_section, examen_fisico_nariz_section,
                          examen_fisico_boca_section,
                          examen_fisico_cuello_section,
                          examen_fisico_torax_pulmones_section,
                          examen_fisico_corazon_section,
                          examen_fisico_abdomen_section,
                          examen_fisico_genito_unitario_section,
                          examen_fisico_columna_section,
                          examen_fisico_extremidades_section,
                          examen_fisico_neurologico_section,
                          conclusion_section)

from docapp.forms import (AudioForm,
                          ananmesis_section,
                          ant_familiar_section,
                          ant_otro_section,
                          exposicion_audifonos_section, exposicion_auto_section, exposicion_moto_section,
                          exposicion_pesada_section,
                          estado_actual_escucha_ruido_section, estado_actual_escucha_section,
                          estado_actual_frases_repetidas_section,
                          estado_actual_ruido_molestia_section, estado_actual_volumen_tv_section,
                          information_section,
                          otoscopia_section)

from .chekers import CheckDoctor
from .customs import FormViewPutExtra, FormsetPostManager, BaseRegisterExamBehavior, BaseExamUpdateBehavior


class RegisterOccupational(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                           FormViewPutExtra):
    model = Occupational
    form_class = OcupaForm
    template_name = 'docapp/register/exams/occupational.html'
    extra_context = {'exam_name': 'ocupacional',
                     'parent_object_key': 'ocupacional',
                     'formsets': [
                         {'section_name': 'ant_familiares',
                          'title': 'Antecedentes Familiares',
                          'form': ant_familiares_section},
                         {'section_name': 'ant_gineco_section',
                          'title': 'Antecedentes Gineco-Obstetricos',
                          'form': ant_gineco_section},
                         # Habitos
                         {'section_name': 'habitos_generales',
                          'title': 'Habitos Generales',
                          'form': habito_general_section},
                         {'section_name': 'habito_alcohol',
                          'title': 'Habito Alcohol',
                          'form': habito_alcohol_section},
                         {'section_name': 'habito_cigarrillo',
                          'title': 'Habito Cigarillo',
                          'form': habito_cigarillo_section},
                         {'section_name': 'habito_droga',
                          'title': 'Habito Droga',
                          'form': habito_droga_section},
                         # Examen Fisico
                         {'section_name': 'aspecto_general',
                          'title': 'Aspecto General',
                          'form': examen_fisico_general_section},
                         # # Organos de los sentidos
                         {'section_name': 'org_boca',
                          'title': 'Boca',
                          'form': examen_fisico_boca_section},
                         {'section_name': 'org_nariz',
                          'title': 'Nariz',
                          'form': examen_fisico_nariz_section},
                         {'section_name': 'org_oidos',
                          'title': 'Oidos',
                          'form': examen_fisico_oidos_section},
                         {'section_name': 'org_ojos',
                          'title': 'Ojos',
                          'form': examen_fisico_ojos_section},

                         # # Fin Organos
                         {'section_name': 'exm_cuello',
                          'title': 'Cuello',
                          'form': examen_fisico_cuello_section},
                         {'section_name': 'exm_torax_pulmones',
                          'title': 'Torax y Pulmones',
                          'form': examen_fisico_torax_pulmones_section},
                         {'section_name': 'exm_corazon',
                          'title': 'Corazon',
                          'form': examen_fisico_corazon_section},
                         {'section_name': 'exm_abdomen',
                          'title': 'Abdomen',
                          'form': examen_fisico_abdomen_section},
                         {'section_name': 'exm_columna',
                          'title': 'Columna',
                          'form': examen_fisico_columna_section},
                         {'section_name': 'exm_extremidades',
                          'title': 'Extremidades',
                          'form': examen_fisico_extremidades_section},
                         {'section_name': 'exm_neurologico',
                          'title': 'Neurologico',
                          'form': examen_fisico_neurologico_section},
                         {'section_name': 'exm_genito_unitario',
                          'title': 'Genito Unitario',
                          'form': examen_fisico_genito_unitario_section},
                         # Fin examen fisico
                         {'section_name': 'conclusiones',
                          'title': 'Conclusiones',
                          'form': conclusion_section}
                     ]
                     }


register_occupational = RegisterOccupational.as_view()


class RegisterAudiology(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                        FormViewPutExtra):
    model = Audiology
    form_class = AudioForm
    template_name = 'docapp/register/exams/audilogy.html'
    extra_context = {'exam_name': 'audiologia',
                     'parent_object_key': 'audiologia',
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
                         # Exposiciones
                         {'section_name': 'exp_audifonos',
                          'title': 'Uso de Audifonos',
                          'form': exposicion_audifonos_section},
                         {'section_name': 'exo_moto',
                          'title': 'Uso de Motocicleta',
                          'form': exposicion_moto_section},
                         {'section_name': 'exp_automotriz',
                          'title': 'Uso de Automotriz',
                          'form': exposicion_auto_section},
                         {'section_name': 'exp_maq_pesada',
                          'title': 'Uso de Maquinaria Pesada',
                          'form': exposicion_pesada_section},
                         # Estado Actual
                         {'section_name': 'est_ruido_molestia',
                          'title': '¿Le molesta el ruido?',
                          'form': estado_actual_ruido_molestia_section},
                         {'section_name': 'est_vol_tv',
                          'title': '¿Debe subir el volumen del televisor?',
                          'form': estado_actual_volumen_tv_section},
                         {'section_name': 'est_fra_repite',
                          'title': '¿En una conversación le repiten las frases?',
                          'form': estado_actual_frases_repetidas_section},
                         {'section_name': 'est_esc_oye',
                          'title': '¿Escucha bien?',
                          'form': estado_actual_escucha_section},
                         {'section_name': 'est_esc_ruido',
                          'title': '¿Escucha bien cuando hay ruido?',
                          'form': estado_actual_escucha_ruido_section},
                         # End Estado Actual
                         {'section_name': 'informacion',
                          'title': 'Informacion',
                          'form': information_section},
                         {'section_name': 'otoscopia',
                          'title': 'Otoscopia',
                          'form': otoscopia_section},
                     ]
                     }


register_audiology = RegisterAudiology.as_view()

"""
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
