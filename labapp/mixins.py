from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.db import IntegrityError, transaction
from django.contrib import messages

from docapp.choices import ExamStates
from labapp.models import ExamResults


class PostResultManager(object):
    def invalid_form(self, result_formset):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(**{'object': self.object,
                                                                'result_formset': result_formset}))

    def post(self, request, *args, **kwargs):
        lab_exam = self.get_object()
        lab_exam.examinacion_id.update_lab()
        result_formset = self.result_formset(request.POST)

        if result_formset.is_valid():
            temp = []
            for form in result_formset:
                if not form.cleaned_data.get('DELETE'):
                    form.cleaned_data.pop('DELETE', None)
                    form.cleaned_data['examen'] = lab_exam
                    temp.append(ExamResults(**form.cleaned_data))
            try:
                with transaction.atomic():
                    ExamResults.objects.filter(examen=lab_exam).delete()
                    ExamResults.objects.bulk_create(temp)
            except IntegrityError:
                messages.error(request=request, message="Error Save Information Check Data")
                return self.invalid_form(result_formset=result_formset)
        else:
            return self.invalid_form(result_formset=result_formset)

        messages.success(request=request, message="Informacion guardada correctamente")
        return HttpResponseRedirect(reverse('labapp:lab_own_examinations'))