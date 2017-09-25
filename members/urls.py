from django.conf.urls import url

from . import views
from django.contrib.auth.views import logout


urlpatterns = [
    url(r'^sign_in/', views.sign_in, name='members.sign_in'),
    url(r'^register/', views.register, name='members.register'),
    url(r'^edit/', views.edit_info,
        name='members.edit_info'),
    url(r'^logout/', logout,
        {'next_page': '/account/sign_in/'},
        name='members.logout'),
    url(r'^change_password/', views.change_password,
        name='members.change_password'),
]
