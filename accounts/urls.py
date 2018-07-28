from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^register/doctor', views.register_doctor, name='register_doctor'),
    url(r'^register/employ', views.register_rec_or_lab, name='register_rec_or_lab'),
]