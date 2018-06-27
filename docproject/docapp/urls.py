from django.conf.urls import url
from docapp.views import example


app_name = 'docapp'
urlpatterns =[
    url(r'^example/$', example, name='example')
]