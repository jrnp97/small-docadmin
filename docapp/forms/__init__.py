from .general import (CompanyForm, PersonForm, AntecedentForm, hazards_inlineformset, ExamForm)

from .visiometria import (VisioForm, sintomas_section, ant_enfermedad_section, ant_uso_lentes_section,
                          ant_extra_exams, agudeza_section, cronomatica_section)

from .audiology import (AudioForm,
                        ananmesis_section,
                        ant_familiar_section,
                        ant_otro_section,
                        exposicion_audifonos_section, exposicion_auto_section, exposicion_moto_section,
                        exposicion_pesada_section,
                        estado_actual_escucha_radio_section, estado_actual_escucha_section,
                        estado_actual_frases_repetidas_section,
                        estado_actual_ruido_molestia_section, estado_actual_volumen_tv_section,
                        information_section,
                        otoscopia_section)

from .occupational import (OcupaForm,
                           ant_familiares_section,
                           ant_gineco_section,
                           habito_alcohol_section, habito_cigarillo_section, habito_droga_section,
                           habito_general_section,
                           exam_fisico_oidos_section, examen_fisico_abdomen_section, examen_fisico_boca_section,
                           examen_fisico_columna_section, examen_fisico_corazon_section, examen_fisico_cuello_section,
                           examen_fisico_extremidades_section, examen_fisico_general_section,
                           examen_fisico_genito_unitario_section, examen_fisico_nariz_section,
                           examen_fisico_neurologico_section, examen_fisico_ojos_section,
                           examen_fisico_torax_pulmones_section, conclusion_section)

from .laboratory import LabForm, blood_section, exams_section
