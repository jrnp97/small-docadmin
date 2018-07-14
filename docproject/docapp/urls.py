from django.conf.urls import url
from docapp import views


app_name = 'docapp'
urlpatterns =[
    url(r'^login/$', views.login, name='login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/ingreso/$', views.ingreso, name='ingreso'),
    url(r'^dashboard/medicos/$', views.doctors, name='medicos'),
    url(r'^dashboard/examenes/general', views.general, name='medicina_general'),
    url(r'^dashboard/examenes/lab', views.laboratorio, name='laboratorio'),
    url(r'^dashboard/examenes/audiometria', views.audiometria, name='audiometria'),
    url(r'^dashboard/examenes/visiometria', views.visiometria, name='visiometria'),

]

# url(r'^login/$', views.Login.as_view(), name='login')
