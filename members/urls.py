from django.conf.urls import url

from . import views
from django.contrib.auth.views import logout


urlpatterns = [
    url(r'^sign_in/', views.sign_in, name='sign_in'),
    url(r'^activate', views.activate, name='activate'),
    url(r'^register/', views.register, name='register'),
    url(r'^success/', views.registration_success.as_view(), name='success'),
    url(r'^edit/', views.edit_info, name='edit_info'),
    url(r'^logout/', logout, {'next_page': '/account/sign_in/'},
        name='logout'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^my_perks/', views.my_perks, name='my_perks'),
]
