from .receptionist import (dashboard,
                           register_company, update_company, detail_company, list_company,
                           register_employ_from_company, register_employ_without_company, update_employ, detail_employ,
                           list_independent_employ, list_employ_company,
                           register_employ_examination, list_examination,
                           register_simple_patient, update_simple_patient, detail_patient, list_simple_patient,
                           make_consulta, list_consults,
                           register_lab, update_lab, deactivate_lab, list_lab, register_lab_admin, update_lab_admin,
                           list_admin_lab, detail_laboratory, deactivate_lab_admin, detail_lab_admin)

from .doctor import (register_occupational, register_audiology, register_visiometry,
                     update_ocupacional, update_audiologia, update_visiometria,
                     register_employ_antecedent, update_employ_antecedent, list_employ_antecedents,
                     detail_employ_antecedent, register_simple_exam, register_altura, update_altura,
                     own_examinations, take_a_exam, end_examinations, doctor_end_exam)

from .general import detail_examination
