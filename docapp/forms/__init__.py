from .general import (CompanyForm, PersonForm, AntecedentForm, hazards_inlineformset, ExamForm)
from .visiometria import (VisioForm, sintomas_section, ant_enfermedad_section, ant_uso_lentes_section,
                          ant_extra_exams, agudeza_section, cronomatica_section)
from .audiology import (AudioForm, ananmesis_section, ant_familiar_section, ant_otro_section, exposicion_section,
                        estado_actual_section)
from .audiometry import (AudiometriaForm, otoscopia_section, information_section)

from .occupational import (OcupaForm, ant_familiares_section, habitos_section, fisico_general_form,
                           organos_sentidos_section, conclusion_section)

from .laboratory import LabForm, blood_section, exams_section
