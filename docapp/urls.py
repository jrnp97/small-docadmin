from django.conf.urls import url
from docapp import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    # Company urls
    url(r'^company/$', views.company_list, name='company_list'),
    url(r'^company/(?P<company_id>[0-9]+)/$', views.detail_company, name='detail_company'),
    url(r'^register/company/$', views.register_company, name='register_company'),
    url(r'^update/company/(?P<company_id>[0-9]+)/$', views.update_company, name='update_company'),
    url(r'^employs/company/(?P<company_id>[0-9])+/$', views.filter_person_list, name='filter_person_list'),

    # Person urls
    url(r'^person/$', views.person_list, name='person_list'),
    url(r'^person/(?P<person_id>[0-9]+)/$', views.detail_person, name='detail_person'),
    url(r'^register/person/$', views.register_person, name='register_person'),
    url(r'^register/person/(?P<company_id>[0-9]+)/$', views.register_employ, name='register_employ'),
    url(r'^update/person/(?P<person_id>[0-9]+)/$', views.update_person, name='update_person'),

    # Antecedent urls
    url(r'^antecedent/(?P<person_id>[0-9])/$', views.person_antecedent_list, name='person_antecedent_list'),
    url(r'^antecedent/detail/(?P<antecedent_id>[0-9]+)/$', views.detail_antecedent, name='detail_antecedent'),
    url(r'^register/antecedent/(?P<person_id>[0-9]+)/$', views.register_antecedent, name='register_antecedent'),
    url(r'^update/antecedent/(?P<antecedent_id>[0-9]+)/$', views.update_antecedent, name='update_antecedent'),

    # Exam urls
    url(r'^register/exam/(?P<person_id>[0-9]+)/$', views.register_exam, name='register_exam'),
    url(r'^exams/$', views.exam_list, name='exam_list'),

    # Registro de examanes
    url(r'^register/(?P<exam_id>[0-9]+)/occupational/$', views.register_occupational, name='register_occupational'),
    url(r'^register/(?P<exam_id>[0-9]+)/audiology/$', views.register_audiology, name='register_audiology'),
    url(r'^register/(?P<exam_id>[0-9]+)/visiometry/$', views.register_visiometry, name='register_visiometry'),
    # Update exams
    url(r'^occupational/(?P<pk>[0-9]+)/$', views.update_ocupacional, name='update_ocupacional'),
    url(r'^audiology/(?P<pk>[0-9]+)/$', views.update_audiologia, name='update_audiologia'),
    url(r'^visiometry/(?P<pk>[0-9]+)/$', views.update_visiometria, name='update_visiometria'),
]
