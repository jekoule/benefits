from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.perk_detail,
        name='perk_detail'),
    url(r'^(?P<category>[\w-]+)/$', views.index, name='category'),
]
