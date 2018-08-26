from .general import (CompanyForm, PacienteEmpresaForm, ExaminacionForm, AntLaboralesForm, AntLabRiesgosForm,
                      hazards_inlineformset, accident_inlineformset, ParticularForm, ConsultaForm,
                      RegisterSingleExamForm, UpdateSimpleExamForm)

from .visiometria import (VisioForm, sintomas_section, ant_enfermedad_section, ant_uso_lentes_section,
                          ant_extra_exams, agudeza_section, cronomatica_section)

from .audiology import (AudioForm,
                        ananmesis_section,
                        ant_familiar_section,
                        ant_otro_section,
                        exposicion_audifonos_section, exposicion_moto_section, exposicion_auto_section,
                        exposicion_pesada_section,
                        estado_actual_ruido_molestia_section, estado_actual_volumen_tv_section,
                        estado_actual_frases_repetidas_section, estado_actual_escucha_section,
                        estado_actual_escucha_ruido_section,
                        audiometria_section)

from .occupational import (OcupaForm,
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
                           columna_cervical_section, columna_dorsal_section, columna_lumbar_section,
                           conclusion_ingreso_section, conclusion_retiro_section, conclusion_periodico_section,
                           conclusion_post_incapacidad_section)

from .altura import AlturaForm, question_section
