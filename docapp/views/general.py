from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect

from docapp.models.general import Examinacion
from docproject.helpers.chekers import CheckDoctor, CheckUser


# Viws to process a examination process
class ListOwnExams(LoginRequiredMixin, CheckDoctor, TemplateView):
    template_name = 'docapp/lists/exam_list.html'

    def get_context_data(self, **kwargs):
        exams = None
        if hasattr(self.request.user.doctor_profile, 'examinaciones'):
            exams = self.request.user.doctor_profile.examinaciones.all()
        kwargs.update({'exam_list': exams})
        return super(ListOwnExams, self).get_context_data(**kwargs)


own_examinations = ListOwnExams.as_view()


class DoctorTakeAExam(LoginRequiredMixin, CheckDoctor, SingleObjectMixin, TemplateView):
    object = None
    pk_url_kwarg = 'exam_id'
    model = Examinacion
    template_name = 'docapp/take_object.html'
    redirect_url = reverse_lazy('docapp:doctor_own_examinations')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        kwargs.update({'redirect_url': self.redirect_url})
        return super(DoctorTakeAExam, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        exam = self.get_object()
        exam.manejador_por = request.user.doctor_profile
        try:
            exam.save()
        except IntegrityError:
            messages.error(message='Examinacion NO Asignada', request=request)
        else:
            messages.success(message='Examinacion Asignada Exitosamente', request=request)
        return HttpResponseRedirect(reverse('docapp:doctor_own_examinations'))


take_a_exam = DoctorTakeAExam.as_view()


class DetailExaminacion(LoginRequiredMixin, CheckUser, DetailView):
    pk_url_kwarg = 'exam_id'
    context_object_name = 'exam'
    model = Examinacion
    template_name = 'docapp/details/examination.html'


detail_examination = DetailExaminacion.as_view()
