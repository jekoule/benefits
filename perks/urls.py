from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='perks.index'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.perk_detail.as_view(),
        name='perks.perk_detail'),
]
