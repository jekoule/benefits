from django.conf.urls import url

from . import views
from django.contrib.auth.views import logout


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^my_perks/', views.my_perks, name='my_perks'),
    url(r'^sign_in/', views.sign_in, name='sign_in'),
    url(r'^logout/', logout, {'next_page': '/partner/'},
        name='logout'),
    url(r'^change_password/', views.change_password, name='change_password'),
]
