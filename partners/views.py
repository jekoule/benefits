# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView


class dashboard(TemplateView):
    template_name = 'partners/dashboard.html'



def sign_in(request):
    pass


def change_password(request):
    pass
