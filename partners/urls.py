from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'partners'

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^my_perks/', views.my_perks, name='my_perks'),
    url(r'^sign_in/', views.sign_in, name='sign_in'),
    url(r'^logout/', auth_views.LogoutView.as_view(),
        {'next_page': '/partner/'}, name='logout'),
    url(r'^change_password/', views.change_password, name='change_password'),
]
