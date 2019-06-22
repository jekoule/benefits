from django.conf.urls import url

from . import views

app_name = 'perks'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.perk_detail.as_view(),
        name='perk_detail'),
    url(r'^modal/(?P<pk>[0-9]+)/$', views.perk_modal,
        name='perk_modal'),
    url(r'^get/(?P<pk>[0-9]+)/$', views.get_perk,
        name='get_perk'),
    url(r'^(?P<category>[\w-]+)/$', views.index, name='category'),
]
