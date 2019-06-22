from django.conf.urls import url

from . import views

app_name = 'customers'

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^delete/$', views.delete_members, name='delete_members'),
    url(r'^delete_ajax/$', views.delete_member_ajax,
        name='delete_member_ajax'),
    url(r'^switch_status_ajax/$', views.switch_status_ajax,
        name='switch_status_ajax'),
    url(r'^add/$', views.add_members, name='add_members'),
]
