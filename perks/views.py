# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Perk, PerkCategory
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView


@login_required(login_url='/members/sign_in/')
def index(request, category=None):
    if category is not None:
        category = get_object_or_404(PerkCategory, slug=category)
        perks = Perk.objects.filter(category=category)
    else:
        perks = Perk.objects.all()
    categories = PerkCategory.objects.all()
    return render(request, 'perks/index.html',
                  {'perks': perks, 'categories': categories,
                   'active_category': category})


class perk_detail(DetailView):

    model = Perk
