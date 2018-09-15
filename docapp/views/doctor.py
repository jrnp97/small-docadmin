from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView, TemplateView, CreateView
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from docapp.models import (PacienteEmpresa, Occupational, Audiology, Visiometry, Altura, AntecedentesLaborales, Riesgos,
                           Accidentes, SimpleExam)
from docapp.forms import (OcupaForm,
                          ant_familiares_section,
                          ant_gineco_section,
                          revision_sistemas_section,
                          biometria_section,
                          habito_alcohol_section, habito_cigarillo_section, habito_droga_section,
                          habito_general_section,
                          examen_fisico_general_section, examen_fisico_abdomen_section, examen_fisico_boca_section,
                          examen_fisico_columna_section, examen_fisico_corazon_section, examen_fisico_cuello_section,
                          examen_fisico_extremidades_section, examen_fisico_genito_unitario_section,
                          examen_fisico_nariz_section, examen_fisico_neurologico_section, examen_fisico_oidos_section,
                          examen_fisico_ojos_section, examen_fisico_torax_pulmones_section,
                          conclusion_ingreso_section,
                          conclusion_periodico_section,
                          conclusion_post_incapacidad_section,
                          conclusion_retiro_section)

from docapp.forms import (AudioForm,
                          ananmesis_section,
                          ant_familiar_section,
                          ant_otro_section,
                          exposicion_audifonos_section, exposicion_moto_section, exposicion_auto_section,
                          exposicion_pesada_section,
                          estado_actual_ruido_molestia_section, estado_actual_volumen_tv_section,
                          estado_actual_frases_repetidas_section, estado_actual_escucha_section,
                          estado_actual_escucha_ruido_section,
                          audiometria_section)

from docapp.forms import (VisioForm, sintomas_section, ant_enfermedad_section, ant_uso_lentes_section,
                          ant_extra_exams, agudeza_section, cronomatica_section,
                          AntLaboralesForm, hazards_inlineformset, accident_inlineformset)

from docapp.forms import AlturaForm, question_section, SimpleExamForm

from docproject.helpers.chekers import CheckDoctor
from docproject.helpers.customs import (FormViewPutExtra, FormsetPostManager, BaseRegisterExamBehavior,
                                        BaseExamUpdateBehavior)


class RegisterOccupational(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                           FormViewPutExtra):
    model = Occupational
    form_class = OcupaForm
    template_name = 'docapp/register/exams/occupational.html'
    extra_context = {'exam_name': 'ocupacional',
                     'parent_object_key': 'ocupacional_id',
                     'child_name': 'ocupacional',
                     'formsets': [
                         {'section_name': 'ant_familiares',
                          'title': 'Antecedentes Familiares',
                          'form': ant_familiares_section},
                         None,
                         {'section_name': 'revision_sistemas',
                          'title': 'Revision por Sistemas',
                          'form': revision_sistemas_section},
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
                         {'section_name': 'biometria',
                          'title': 'Biometria',
                          'form': biometria_section},
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
                         None
                     ]
                     }

    def get_context_data(self, **kwargs):
        examination = self.get_object()
        examination_patient = self.get_object().paciente_id
        if examination_patient.sexo == 'femenino':
            self.extra_context['formsets'][1] = {'section_name': 'ant_gineco',
                                                 'title': 'Antecedentes Gineco-Obstricos',
                                                 'form': ant_gineco_section}
        conclusion_section = {'section_name': 'conclusion',
                              'title': 'Conclusion',
                              'form': None}
        if examination.tipo == 'ingreso':
            conclusion_section.update({'form': conclusion_ingreso_section})
        elif examination.tipo == 'periodico':
            conclusion_section.update({'form': conclusion_periodico_section})
        elif examination.tipo == 'retiro' or examination.tipo == 'reubicacion':
            conclusion_section.update({'form': conclusion_retiro_section})
        elif examination.tipo == 'post-incapacidad':
            conclusion_section.update({'form': conclusion_post_incapacidad_section})
        else:
            raise SuspiciousOperation("Contact Admin")

        self.extra_context['formsets'][21] = conclusion_section

        return super(RegisterOccupational, self).get_context_data(**kwargs)


register_occupational = RegisterOccupational.as_view()


class UpdateOccupational(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Occupational
    form_class = OcupaForm
    template_name = 'docapp/register/exams/occupational.html'
    extra_context = {'exam_name': 'ocupacional',
                     'parent_object_key': 'ocupacional_id',
                     'formsets': [
                         {'section_name': 'ant_familiares',
                          'title': 'Antecedentes Familiares',
                          'form': ant_familiares_section},
                         # TODO Antecedent gineco-obstetricos put depend sex of pacient
                         {'section_name': 'revision_sistemas',
                          'title': 'Revision por Sistemas',
                          'form': revision_sistemas_section},
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
                         {'section_name': 'biometria',
                          'title': 'Biometria',
                          'form': biometria_section},
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
                         # TODO Section conclusion process depend examination type
                     ]
                     }

    def get_context_data(self, **kwargs):
        return super(UpdateOccupational, self).get_context_data(**kwargs)


update_ocupacional = UpdateOccupational.as_view()


class RegisterAudiology(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                        FormViewPutExtra):
    model = Audiology
    form_class = AudioForm
    template_name = 'docapp/register/exams/audilogy.html'
    extra_context = {'exam_name': 'audiologia',
                     'parent_object_key': 'audiologia_id',
                     'child_name': 'audiologia',
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
                         {'section_name': 'audiometria',
                          'title': 'Audiometria',
                          'form': audiometria_section},
                     ]
                     }


register_audiology = RegisterAudiology.as_view()


class UpdateAudiology(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Audiology
    form_class = AudioForm
    template_name = 'docapp/register/exams/audilogy.html'
    extra_context = {'exam_name': 'audiologia',
                     'parent_object_key': 'audiologia_id',
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
                         {'section_name': 'audiometria',
                          'title': 'Audiometria',
                          'form': audiometria_section},
                     ]
                     }


update_audiologia = UpdateAudiology.as_view()


class RegisterVisiometry(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager,
                         FormViewPutExtra):
    model = Visiometry
    form_class = VisioForm
    template_name = 'docapp/register/exams/visiometry.html'
    success_url = reverse_lazy('docapp:list_examination')
    extra_context = {'exam_name': 'visiometria',
                     'parent_object_key': 'visiometria_id',
                     'child_name': 'visiometria',
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
                          'title': 'Antecedentes de Examenes',
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


class UpdateVisiometry(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Visiometry
    form_class = VisioForm
    template_name = 'docapp/register/exams/visiometry.html'
    extra_context = {'exam_name': 'visiometria',
                     'parent_object_key': 'visiometria_id',
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
                          'title': 'Antecedentes de Examenes',
                          'form': ant_extra_exams},

                         {'section_name': 'agudeza',
                          'title': 'Agudeza',
                          'form': agudeza_section},

                         {'section_name': 'cronomatica',
                          'title': 'Cronomatica',
                          'form': cronomatica_section}
                     ]
                     }


update_visiometria = UpdateVisiometry.as_view()


class RegisterAltura(LoginRequiredMixin, CheckDoctor, BaseRegisterExamBehavior, FormsetPostManager, FormViewPutExtra):
    model = Altura
    form_class = AlturaForm
    template_name = 'docapp/register/exams/altura.html'
    extra_context = {'exam_name': 'altura',
                     'parent_object_key': 'altura_id',
                     'child_name': 'altura',
                     'formsets': [
                         {'section_name': 'preguntas',
                          'title': 'Estado',
                          'form': question_section},
                     ]
                     }


register_altura = RegisterAltura.as_view()


class UpdateAltura(LoginRequiredMixin, CheckDoctor, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Altura
    form_class = AlturaForm
    template_name = 'docapp/register/exams/altura.html'
    extra_context = {'exam_name': 'altura',
                     'parent_object_key': 'altura_id',
                     'formsets': [
                         {'section_name': 'preguntas',
                          'title': 'Estado',
                          'form': question_section},
                     ]
                     }


update_altura = UpdateAltura.as_view()


class RegisterSimpleExam(LoginRequiredMixin, CheckDoctor, UpdateView):
    model = SimpleExam
    form_class = SimpleExamForm
    template_name = 'docapp/register/exams/simple.html'
    success_url = reverse_lazy('docapp:list_examination')


register_simple_exam = RegisterSimpleExam.as_view()


# Process employ antecedent
class RegisterEmployAntecedent(CheckDoctor, LoginRequiredMixin, FormsetPostManager, FormViewPutExtra):
    pk_url_kwarg = 'person_id'
    form_class = AntLaboralesForm
    model = AntecedentesLaborales
    template_name = 'docapp/register/antecedent.html'
    success_url = reverse_lazy('docapp:dashboard')
    model_to_filter = PacienteEmpresa
    context_object_2_name = 'person'
    extra_context = {'exam_name': 'Antecedente',
                     'parent_object_key': 'antecedente_id',
                     'formsets': [
                         {'section_name': 'riesgos',
                          'title': 'Riesgos',
                          'form': hazards_inlineformset},
                         {'section_name': 'accidentes',
                          'title': 'Accidentes',
                          'form': accident_inlineformset}
                     ]
                     }

    def _custom_save(self, form):
        person = self.get_object()
        form.create_by = self.request.user.doctor_profile
        form.person = person
        instance = form.save()
        if instance:
            person_name = person.__str__()
            messages.success(self.request, message=f"Antecedente de {person_name} register exitosamente")
        return instance


register_employ_antecedent = RegisterEmployAntecedent.as_view()


class UpdateEmployAntecedent(CheckDoctor, LoginRequiredMixin, FormsetPostManager, UpdateView):
    pk_url_kwarg = 'antecedent_id'
    context_object_name = 'antecedent'
    model = AntecedentesLaborales
    form_class = AntLaboralesForm
    template_name = 'docapp/register/antecedent.html'
    success_url = reverse_lazy('docapp:dashboard')
    extra_context = {'parent_object_key': 'antecedente_id',
                     'formsets': [
                         {'section_name': 'riesgos',
                          'title': 'Riesgos',
                          'form': hazards_inlineformset},
                         {'section_name': 'accidentes',
                          'title': 'Accidentes',
                          'form': accident_inlineformset}
                     ]
                     }

    def form_valid(self, form):
        """ Overwrite form_valid to add missing information"""
        antecedent = self.get_object()
        form.create_by = self.request.user.doctor_profile
        form.person = antecedent.persona
        return super(UpdateEmployAntecedent, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """ Overwrite get_context_data method to append formset necessary"""
        antecedent = self.get_object()
        try:
            data = Riesgos.objects.get(antecedente_id=antecedent)
            dict_data = vars(data)
            # Delete unneeded info
            dict_data.pop('_state', None)
            dict_data.pop('id', None)
            hazard_initial_data = [dict_data]
        except ObjectDoesNotExist:
            hazard_initial_data = []
        try:
            data = Accidentes.objects.filter(antecedente_id=antecedent)
            accident_initial_data = []
            for element in data:
                dict_data = vars(element)
                # Delete unneeded info
                dict_data.pop('_state', None)
                dict_data.pop('id', None)
                accident_initial_data.append(dict_data)
        except ObjectDoesNotExist:
            accident_initial_data = []

        accident_formset = forms.inlineformset_factory(parent_model=AntecedentesLaborales, model=Accidentes,
                                                       extra=len(accident_initial_data), can_delete=True,
                                                       fields='__all__', exclude=('registrado_por',))

        self.extra_context = {'parent_object_key': 'antecedente_id',
                              'formsets': [
                                  {'section_name': 'riesgos',
                                   'title': 'Riesgos',
                                   'form': hazards_inlineformset(initial=hazard_initial_data)},
                                  {'section_name': 'accidentes',
                                   'title': 'Accidentes',
                                   'form': accident_formset(initial=accident_initial_data)}
                              ]
                              }
        kwargs.update(self.extra_context)
        return super(UpdateEmployAntecedent, self).get_context_data(**kwargs)


update_employ_antecedent = UpdateEmployAntecedent.as_view()


class ListEmployAntecedents(CheckDoctor, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'person_id'
    context_object_name = 'paciente'
    model = PacienteEmpresa
    template_name = 'docapp/lists/antecedent_list.html'


list_employ_antecedents = ListEmployAntecedents.as_view()


class DetailEmployAntecedent(CheckDoctor, LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'antecedent_id'
    model = AntecedentesLaborales
    context_object_name = 'antecedent'
    template_name = 'docapp/details/antecedent.html'


detail_employ_antecedent = DetailEmployAntecedent.as_view()
# End employ antecedent
