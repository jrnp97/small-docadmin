from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, ListView, TemplateView
from django.core.urlresolvers import reverse_lazy

from docproject.helpers.chekers import CheckLaboratory

from labapp.forms import BaseLabUserCreateForm
from docapp.models import Examinacion


class RegisterPersonal(LoginRequiredMixin, CheckLaboratory, SuccessMessageMixin, FormView):
    form_class = BaseLabUserCreateForm
    success_url = reverse_lazy('docapp:dashboard')
    success_message = 'Personal de laboratorio registrado exitosamente'


register_personal = RegisterPersonal.as_view()


class ListExaminationWithouLab(LoginRequiredMixin, CheckLaboratory, ListView):
    model = Examinacion
    template_name = 'docapp/lists/exam_list.html'

    def get_queryset(self):
        # queryset = Examinacion.objects.filter(laboratorio_id=None)
        user_lab = self.request.user.laboratory_profile.laboratorio_id
        return self.model._default_manager.filter(laboratorio_id=user_lab)


list_examination_todo = ListExaminationWithouLab.as_view()


# Viws to process a examination process
class ListOwnExams(LoginRequiredMixin, CheckLaboratory, TemplateView):
    template_name = 'docapp/lists/exam_list.html'

    def get_context_data(self, **kwargs):
        exams = None
        if hasattr(self.request.user.laboratory_profile, 'examinaciones'):
            exams = self.request.user.laboratory_profile.examinaciones.all()
        kwargs.update({'exam_list': exams})
        return super(ListOwnExams, self).get_context_data(**kwargs)


lab_own_examinations = ListOwnExams.as_view()