
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='customers.dashboard'),
    url(r'^delete/$', views.delete_members, name='customers.delete_members'),
    url(r'^add/$', views.add_members, name='customers.add_members'),
]
