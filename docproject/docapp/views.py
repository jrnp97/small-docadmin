from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import LoginView


# Create your views here.
def dashboard(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin:login')
    else:
        context = dict({
            'routes': ['Inicio'],
            'page_header': 'Dashboard Proof',
            'active': 'inicio',
            'exam_collapse': True,
        })
        return render(request, 'docapp/home.html', context)


def ingreso(request):
    context = dict({
        'routes': ['Ingreso'],
        'page_header': 'Dashboard Proof',
        'active': 'ingreso',
        'exam_collapse': True,
    })
    return render(request, 'docapp/ingreso.html', context)


def doctors(request):
    context = dict({
        'routes': ['Medicos'],
        'page_header': 'Dashboard Proof',
        'active': 'doctors',
        'exam_collapse': True,
    })
    return render(request, 'docapp/doctors.html', context)


# Exams views
def general(request):
    context = dict({
        'routes': ['Examenes', 'Medicina General'],
        'page_header': 'Dashboard Proof',
        'active': 'medicina_general',
        'exam_collapse': False,
    })
    return render(request, 'docapp/exams/medicina_general.html', context)


def laboratorio(request):
    context = dict({
        'routes': ['Examenes', 'Laboratorio'],
        'page_header': 'Dashboard Proof',
        'active': 'laboratorio',
        'exam_collapse': False,
    })
    return render(request, 'docapp/exams/laboratorio.html', context)


def visiometria(request):
    context = dict({
        'routes': ['Examenes', 'Visiometria'],
        'page_header': 'Dashboard Proof',
        'active': 'visiometria',
        'exam_collapse': False,
    })
    return render(request, 'docapp/exams/visiometria.html', context)


def audiometria(request):
    context = dict({
        'routes': ['Examenes', 'Audiometria'],
        'page_header': 'Dashboard Proof',
        'active': 'audiometria',
        'exam_collapse': False,
    })
    return render(request, 'docapp/exams/audiometria.html', context)


class Login(LoginView):
    template_name = 'docapp/login.html'
    redirect_authenticated_user = True


login = Login.as_view()
