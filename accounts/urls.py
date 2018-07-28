from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/doctor', views.register_doctor, name='register_doctor'),
    url(r'^register/receptionist', views.register_rec, name='register_rec'),
    url(r'^register/laboratory', views.register_lab, name='register_lab'),
    url(r'^update/doctor/(?P<user_id>[0-9]+)/$', views.update_doctor, name='update_doctor'),
    url(r'^update/receptionist/(?P<user_id>[0-9]+)/$', views.update_rec, name='update_rec'),
    url(r'^update/laboratory/(?P<user_id>[0-9]+)/$', views.update_lab, name='update_lab'),
    url(r'^delete/doctor/(?P<user_id>[0-9]+)/$', views.delete_doctor, name='delete_doctor'),
    url(r'^delete/receptionist/(?P<user_id>[0-9]+)/$', views.delete_rec, name='delete_rec'),
    url(r'^delete/laboratory/(?P<user_id>[0-9]+)/$', views.delete_lab, name='delete_lab'),
    url(r'^doctor/(?P<user_id>[0-9]+)/$', views.show_doctor, name='show_doctor'),
    url(r'^receptionist/(?P<user_id>[0-9]+)/$', views.show_rec, name='show_rec'),
    url(r'^laboratory/(?P<user_id>[0-9]+)/$', views.show_lab, name='show_lab')
]
