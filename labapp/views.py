from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, ListView, TemplateView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q, Count
from django.views.generic.detail import SingleObjectMixin
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect
from django import forms

from docapp.choices import ExamStates
from docproject.helpers.chekers import CheckLaboratory

from labapp.forms import BaseLabUserCreateForm, lab_exam_result
from docapp.models import Examinacion
from labapp.models import LabExam, ExamResults, Laboratorio
from labapp.mixins import PostResultManager


class RegisterPersonal(LoginRequiredMixin, CheckLaboratory, SuccessMessageMixin, FormView):
    form_class = BaseLabUserCreateForm
    success_url = reverse_lazy('docapp:dashboard')
    success_message = 'Personal de laboratorio registrado exitosamente'


register_personal = RegisterPersonal.as_view()


class ListExaminationWithouLab(LoginRequiredMixin, CheckLaboratory, ListView):
    model = Examinacion
    context_object_name = 'exam_list'
    template_name = 'docapp/lists/exam_list.html'

    def get_queryset(self):
        user_lab = self.request.user.laboratory_profile.laboratorio_id
        queryset = Examinacion.objects.filter(
            Q(examenes_laboratorios__laboratorio_id=user_lab) & Q(examenes_laboratorios__manejado_por=None)
        ).annotate(dcount=Count('tipo'))
        return queryset


list_examination_todo = ListExaminationWithouLab.as_view()


# Viws to process a examination process
class ListOwnExams(LoginRequiredMixin, CheckLaboratory, ListView):
    model = Examinacion
    context_object_name = 'exam_list'
    template_name = 'docapp/lists/exam_list.html'

    def get_queryset(self):
        user_lab = self.request.user.laboratory_profile.laboratorio_id
        user = self.request.user.laboratory_profile
        queryset = Examinacion.objects.filter(
            Q(examenes_laboratorios__laboratorio_id=user_lab) & Q(examenes_laboratorios__manejado_por=user)
        ).annotate(dcount=Count('tipo')).exclude(lab_estado=ExamStates.FINALIZADO)
        # Simulate group by clause -- https://stackoverflow.com/questions/629551/how-to-query-as-group-by-in-django
        # https://docs.djangoproject.com/en/dev/topics/db/aggregation/#topics-db-aggregation
        return queryset


lab_own_examinations = ListOwnExams.as_view()


class LabTakeAExam(LoginRequiredMixin, CheckLaboratory, SingleObjectMixin, TemplateView):
    object = None
    pk_url_kwarg = 'exam_id'
    model = Examinacion
    template_name = 'labapp/take_exam.html'
    redirect_url = reverse_lazy('labapp:lab_own_examinations')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        kwargs.update({'redirect_url': self.redirect_url})
        return super(LabTakeAExam, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        exam = self.get_object()
        exam.lab_estado = ExamStates.ASIGNADO
        exam.save()
        for lab_exam in exam.examenes_laboratorios.all():
            lab_exam.manejado_por = request.user.laboratory_profile
            try:
                lab_exam.save(update_state=False)
            except IntegrityError as e:
                print("Error save infor -> {}".format(e))
                messages.error(message='Examinacion NO Asignada', request=request)
                break
        else:
            messages.success(message='Examinacion Asignada Exitosamente', request=request)
        return HttpResponseRedirect(reverse('labapp:lab_own_examinations'))


lab_take_a_exam = LabTakeAExam.as_view()


class RegisterLabExamResult(LoginRequiredMixin, CheckLaboratory, PostResultManager, DetailView):
    model = LabExam
    context_object_name = 'exam'
    template_name = 'labapp/register/labexam_result.html'
    result_formset = lab_exam_result

    def get_context_data(self, **kwargs):
        if kwargs.get('result_formset') is None:
            kwargs.update({'result_formset': self.result_formset})
        return super(RegisterLabExamResult, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        results = ExamResults.objects.filter(examen=self.get_object()) or None
        if results:
            return HttpResponseRedirect(reverse('labapp:update_lab_exam_result', kwargs=kwargs))
        return super(RegisterLabExamResult, self).get(request, *args, **kwargs)


register_lab_exam_result = RegisterLabExamResult.as_view()


class UpdateLabExamResult(LoginRequiredMixin, CheckLaboratory, PostResultManager, DetailView):
    model = LabExam
    context_object_name = 'exam'
    template_name = 'labapp/register/labexam_result.html'
    result_formset = lab_exam_result

    def get_context_data(self, **kwargs):
        if kwargs.get('result_formset') is None:
            results = ExamResults.objects.filter(examen=self.get_object())
            data_key = ('prueba', 'referencias', 'resultados',)
            initial_data = []
            for result in results:
                all_dict = vars(result)
                data = {key: value for key, value in all_dict.items() if key in data_key}
                initial_data.append(data)

            result_formset = forms.inlineformset_factory(parent_model=LabExam, model=ExamResults, fields='__all__',
                                                         extra=len(initial_data), can_delete=True, exclude=('examen',))
            kwargs.update({'result_formset': result_formset(initial=initial_data)})
        return super(UpdateLabExamResult, self).get_context_data(**kwargs)


update_lab_exam_result = UpdateLabExamResult.as_view()


class LabEndExam(LoginRequiredMixin, CheckLaboratory, SingleObjectMixin, TemplateView):
    object = None
    pk_url_kwarg = 'exam_id'
    model = Examinacion
    template_name = 'docapp/end_process.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(LabEndExam, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        exam = self.get_object()
        if exam.get_lab_process() == 100:
            exam.lab_estado = ExamStates.FINALIZADO
            try:
                exam.save()
            except IntegrityError:
                messages.error(message='Examinacion NO Terminada', request=request)
            else:
                messages.success(message='Examinacion Asignada Exitosamente', request=request)
            return redirect('labapp:lab_end_examinations')
        else:
            messages.warning(request, "No ha terminado todos los examenes")
            return redirect(request.path)


lab_end_exam = LabEndExam.as_view()


class ListEndExams(LoginRequiredMixin, CheckLaboratory, ListView):
    model = Examinacion
    context_object_name = 'exam_list'
    template_name = 'docapp/lists/exam_list.html'

    def get_queryset(self):
        user_lab = self.request.user.laboratory_profile.laboratorio_id
        user = self.request.user.laboratory_profile
        queryset = Examinacion.objects.filter(
            Q(examenes_laboratorios__laboratorio_id=user_lab) & Q(examenes_laboratorios__manejado_por=user) &
            Q(lab_estado='finalizado')
        ).annotate(dcount=Count('tipo'))
        # Simulate group by clause -- https://stackoverflow.com/questions/629551/how-to-query-as-group-by-in-django
        # https://docs.djangoproject.com/en/dev/topics/db/aggregation/#topics-db-aggregation
        return queryset


lab_end_examinations = ListEndExams.as_view()
