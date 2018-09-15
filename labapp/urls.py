from django.conf.urls import url
from labapp import views

urlpatterns = [
    url('^register/personal/$', views.register_personal, name='register_personal'),
    url('^list/examinations/$', views.list_examination_todo, name='list_examination_todo'),
    url('^my/examinations/$', views.lab_own_examinations, name='lab_own_examinations')
]
