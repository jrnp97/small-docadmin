from django.conf.urls import url
from docapp import views


app_name = 'docapp'
urlpatterns =[
    url(r'^/$', views.index, name='index'),
    url(r'^login/$', views.login, name='login')
]

# url(r'^login/$', views.Login.as_view(), name='login')
