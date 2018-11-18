from django.conf.urls import url
from labapp import views

urlpatterns = [
    url('^register/personal/$', views.register_personal, name='register_personal'),
    url('^list/examinations/$', views.list_examination_todo, name='list_examination_todo'),
    url('^my/examinations/$', views.lab_own_examinations, name='lab_own_examinations'),
    url('^take/examination/(?P<exam_id>[0-9]+)/$', views.lab_take_a_exam, name='lab_take_a_exam'),
    url('^register/result/(?P<pk>[0-9]+)/$', views.register_lab_exam_result, name='register_lab_exam_result'),
    url('^update/results/(?P<pk>[0-9]+)/$', views.update_lab_exam_result, name='update_lab_exam_result'),
    url('^end/examination/(?P<exam_id>[0-9]+)/$', views.lab_end_exam, name='lab_end_exam'),
    url('^end/examinations/$', views.lab_end_examinations, name='lab_end_examinations')
]
