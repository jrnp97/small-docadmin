from django.conf.urls import url
from docapp import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    # Company urls
    url(r'^company/$', views.list_company, name='list_company'),
    url(r'^company/(?P<company_id>[0-9]+)/$', views.detail_company, name='detail_company'),
    url(r'^register/company/$', views.register_company, name='register_company'),
    url(r'^update/company/(?P<company_id>[0-9]+)/$', views.update_company, name='update_company'),
    url(r'^employs/company/(?P<company_id>[0-9])+/$', views.list_employ_company, name='list_employ_company'),

    # Employ urls
    url(r'^person/$', views.list_independent_employ, name='list_independent_employ'),
    url(r'^person/(?P<person_id>[0-9]+)/$', views.detail_employ, name='detail_employ'),
    url(r'^register/person/$', views.register_employ_without_company, name='register_employ_without_company'),
    url(r'^register/person/(?P<company_id>[0-9]+)/$', views.register_employ_from_company,
        name='register_employ_from_company'),
    url(r'^update/person/(?P<person_id>[0-9]+)/$', views.update_employ, name='update_employ'),

    # Particular urls
    url(r'^patient/$', views.list_simple_patient, name='list_simple_patient'),
    url(r'^patient/(?P<pk>[0-9]+)/$', views.detail_patient, name='detail_patient'),
    url(r'^register/patient/$', views.register_simple_patient, name='register_simple_patient'),
    url(r'^update/patient/(?P<pk>[0-9]+)/$', views.update_simple_patient, name='update_simple_patient'),

    # Antecedent urls
    url(r'^antecedent/(?P<person_id>[0-9])/$', views.list_employ_antecedents, name='list_employ_antecedents'),
    url(r'^antecedent/detail/(?P<antecedent_id>[0-9]+)/$', views.detail_employ_antecedent,
        name='detail_employ_antecedent'),
    url(r'^register/antecedent/(?P<person_id>[0-9]+)/$', views.register_employ_antecedent,
        name='register_employ_antecedent'),
    url(r'^update/antecedent/(?P<antecedent_id>[0-9]+)/$', views.update_employ_antecedent,
        name='update_employ_antecedent'),

    # Examination urls
    url(r'^register/exam/(?P<person_id>[0-9]+)/$', views.register_employ_examination,
        name='register_employ_examination'),
    url(r'^examination/$', views.list_examination, name='list_examination'),
    url(r'^examination/(?P<exam_id>[0-9]+)/$', views.detail_examination, name='detail_examination'),
    url(r'^take/examination/(?P<exam_id>[0-9]+)/$', views.take_a_exam, name='doctor_take_a_exam'),
    url(r'^my/examinations/$', views.own_examinations, name='doctor_own_examinations'),
    url(r'^end/examination/(?P<exam_id>[0-9]+)/$', views.doctor_end_exam, name='doctor_end_exam'),
    url(r'^end/examinations/$', views.end_examinations, name='doctor_end_examinations'),


    # Registro de examanes
    url(r'^register/(?P<exam_id>[0-9]+)/occupational/$', views.register_occupational, name='register_occupational'),
    url(r'^register/(?P<exam_id>[0-9]+)/audiology/$', views.register_audiology, name='register_audiology'),
    url(r'^register/(?P<exam_id>[0-9]+)/visiometry/$', views.register_visiometry, name='register_visiometry'),
    url(r'^register/(?P<exam_id>[0-9]+)/altura/$', views.register_altura, name='register_altura'),

    # Update exams
    url(r'^occupational/(?P<pk>[0-9]+)/$', views.update_ocupacional, name='update_ocupacional'),
    url(r'^audiology/(?P<pk>[0-9]+)/$', views.update_audiologia, name='update_audiologia'),
    url(r'^visiometry/(?P<pk>[0-9]+)/$', views.update_visiometria, name='update_visiometria'),
    url(r'^altura/(?P<pk>[0-9]+)/$', views.update_altura, name='update_altura'),
    url(r'^simple_exam/(?P<pk>[0-9]+)/$', views.register_simple_exam, name='register_simple_exam'),

    # Lab urls
    url(r'^labs/$', views.list_lab, name='list_lab'),
    url(r'^lab/(?P<pk>[0-9]+)/admin/$', views.list_admin_lab, name='list_admin_lab'),
    url(r'^register/lab/$', views.register_lab, name='register_lab'),
    url(r'^update/lab/(?P<lab_id>[0-9])/$', views.update_lab, name='update_lab'),
    url(r'^deactivate/lab/(?P<lab_id>[0-9])/$', views.deactivate_lab, name='deactivate_lab'),
    url(r'^register/lab/(?P<lab_id>[0-9]+)/admin/$', views.register_lab_admin, name='register_lab_admin'),
    url(r'^update/lab/admin/(?P<pk>[0-9]+)/$', views.update_lab_admin, name='update_lab_admin'),
    url(r'^delete/lab/admin/(?P<pk>[0-9]+)/$', views.deactivate_lab_admin, name='deactivate_lab_admin'),
    url(r'^lab/admin/(?P<pk>[0-9]+)/$', views.detail_lab_admin, name='detail_lab_admin'),
    url('^laboratory/(?P<lab_id>[0-9]+)/$', views.detail_laboratory, name='detail_laboratory')
]
