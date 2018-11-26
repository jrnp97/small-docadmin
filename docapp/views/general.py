from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from django.db import IntegrityError
from django.http import JsonResponse

from accounts.models import DoctorProfile, ReceptionProfile
from docapp.models import Examinacion, Empresa, Consulta, PacienteEmpresa, PacienteParticular
from labapp.models import LaboratoryProfile, Laboratorio
from docproject.helpers.chekers import CheckUser


# Viws to process a examination process
class DetailExaminacion(LoginRequiredMixin, CheckUser, DetailView):
    pk_url_kwarg = 'exam_id'
    context_object_name = 'exam'
    model = Examinacion
    template_name = 'docapp/details/examination.html'


detail_examination = DetailExaminacion.as_view()


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'docapp/dashboard.html'


dashboard = Dashboard.as_view()


class DashboardEAdmin(LoginRequiredMixin, TemplateView):
    template_name = 'docapp/dashboard.html'

    def get_context_data(self, **kwargs):
        doctors = DoctorProfile.objects.all()
        receptionist = ReceptionProfile.objects.all()
        lab_p = LaboratoryProfile.objects.all()
        companies = Empresa.objects.all()
        labs = Laboratorio.objects.all()
        exams = Examinacion.objects.all()
        consults = Consulta.objects.all()
        boxes = [
            {
                'number': doctors.filter(user_id__is_active=True).count(),
                'label': 'Doctores',
                'icon': 'fa-users'
            },
            {
                'number': receptionist.filter(user_id__is_active=True).count(),
                'label': 'Recepcionistas',
                'icon': 'fa-users'
            },
            {
                'number': lab_p.filter(user_id__is_active=True).count(),
                'label': 'Laboratoristas',
                'icon': 'fa-users'
            },
            {
                'number': exams.count(),
                'label': 'Examinaciones',
                'icon': 'fa-id-badge'
            },
            {
                'number': consults.count(),
                'label': 'Consultas',
                'icon': 'fa-id-badge'
            },
            {
                'number': companies.count(),
                'label': 'Empresas Activas',
                'icon': 'fa-building'
            },
            {
                'number': labs.filter(is_active=True).count(),
                'label': 'Laboratorios',
                'icon': 'fa-flask'
            },
        ]
        kwargs.update({'boxes': boxes})
        tables = [
            {'data': doctors.order_by('user_id__date_joined')[:4], 'title': 'Doctores'},
            {'data': receptionist.order_by('user_id__date_joined')[:4], 'title': 'Recepcionistas'},
            {'data': lab_p.order_by('user_id__date_joined')[:4], 'title': 'Laboratoristas'},
            {'data': exams.order_by('fecha_de_creacion')[:4], 'title': 'Examinaciones'},
            {'data': consults.order_by('fecha_de_creacion')[:4], 'title': 'Consultas'},
            {'data': companies.order_by('fecha_de_creacion')[:4], 'title': 'Empresas'},
            {'data': labs.order_by('fecha_de_creacion')[:4], 'title': 'Laboratorios'},
        ]
        kwargs.update({'tables': tables})
        return super(DashboardEAdmin, self).get_context_data(**kwargs)


dashboard_eadmin = DashboardEAdmin.as_view()


def person_filter(request):
    if request.is_ajax():
        identification = request.POST.get('identification')
        if identification:
            try:
                patients = PacienteParticular.objects.filter(identificacion__exact=identification)
                employes = PacienteEmpresa.objects.filter(identificacion__exact=identification)
            except IntegrityError:
                return JsonResponse({'message': 'Registros no encontradas'}, status=404)
            else:
                response = {'patient_count': patients.count(), 'employ_count': employes.count()}
                results = []

                if patients:
                    for patient in patients:
                        results.append({'name': patient.__str__(), 'detail_url': ''})

                if employes:
                    for employ in employes:
                        results.append({'name': employ.__str__(),
                                        'detail_url': reverse('docapp:detail_employ', kwargs={'person_id': employ.id})})

                response.update({'result': results})
                return JsonResponse(response, status=200)
        else:
            return JsonResponse({'message': 'Por favor valide la informacion suministrada'}, status=503)
