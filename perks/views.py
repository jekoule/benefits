# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Perk
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView


@login_required(login_url='/members/sign_in/')
def index(request):
    perks = Perk.objects.all()
    return render(request, 'perks/index.html', {'perks': perks})


class perk_detail(DetailView):

    model = Perk

    def get_context_data(self, **kwargs):
        context = super(perk_detail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
