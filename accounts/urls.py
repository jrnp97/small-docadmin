from django.conf.urls import url
from accounts import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/personal', views.register_personal, name='register_personal'),
    url(r'^update/personal/(?P<user_id>[0-9]+)/$', views.update_personal, name='update_personal'),
    url(r'^deleter/personal/(?P<user_id>[0-9]+)/$', views.delete_personal, name='delete_personal'),
    url(r'^personal/(?P<user_id>[0-9]+)/$', views.detail_personal, name='detail_personal'),

    url(r'^update/profile/$', views.update_profile, name='update_profile'),
    url(r'^profile/$', views.show_profile, name='show_profile'),

    url(r'^users/$', views.user_list, name='user_list')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
