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
class DetailExaminacion(LoginRequiredMixin, CheckUser, DetailView):
    pk_url_kwarg = 'exam_id'
    context_object_name = 'exam'
    model = Examinacion
    template_name = 'docapp/details/examination.html'


detail_examination = DetailExaminacion.as_view()
