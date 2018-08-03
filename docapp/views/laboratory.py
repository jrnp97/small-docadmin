from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from docapp.models import Laboratory
from docapp.forms import LabForm, blood_section, habitos_section, exams_section

from .chekers import CheckLaboratory
from .customs import FormsetPostManager, FormViewPutExtra, BaseRegisterExamBehavior, BaseExamUpdateBehavior


class RegisterLaboratory(LoginRequiredMixin, CheckLaboratory, BaseRegisterExamBehavior, FormsetPostManager,
                         FormViewPutExtra):
    model = Laboratory
    form_class = LabForm
    extra_context = {'exam_name': 'laboratorio',
                     'parent_object_key': 'laboratory',
                     'blood_section': blood_section,
                     'habitos_section': habitos_section,
                     'exams_section': exams_section,
                     }
    template_name = 'docapp/register/laboratory_formsets.html'


register_laboratory = RegisterLaboratory.as_view()


class UpdateLaboratory(LoginRequiredMixin, CheckLaboratory, BaseExamUpdateBehavior, FormsetPostManager, UpdateView):
    model = Laboratory
    form_class = LabForm
    extra_context = {'exam_name': 'laboratorio',
                     'parent_object_key': 'laboratory',
                     'blood_section': blood_section,
                     'habitos_section': habitos_section,
                     'exams_section': exams_section,
                     }
    template_name = 'docapp/register/laboratory_formsets.html'


update_laboratory = UpdateLaboratory.as_view()