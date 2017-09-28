
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^delete/$', views.delete_members, name='delete_members'),
    url(r'^add/$', views.add_members, name='add_members'),
]
