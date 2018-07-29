from django.conf.urls import url
from docapp import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    # Company urls
    url(r'^company/$', views.company_list, name='company_list'),
    url(r'^company/(?P<company_id>[0-9]+)/$', views.detail_company, name='detail_company'),
    url(r'^register/company/$', views.register_company, name='register_company'),
    url(r'^update/company/(?P<company_id>[0-9]+)/$', views.update_company, name='update_company'),
    # Person urls
    url(r'^people/$', views.person_list, name='person_list'),
    url(r'^person/(?P<person_id>[0-9]+)/$', views.detail_person, name='detail_person'),
    url(r'^register/person/$', views.register_person, name='register_person'),
    url(r'^update/person/(?P<person_id>[0-9]+)/$', views.update_person, name='update_person'),
    # Antecedent urls
    url(r'^antecedent/(?P<person_id>[0-9])/$', views.person_antecedent_list, name='person_antecedent_list')

]
