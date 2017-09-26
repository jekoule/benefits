# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Perk, PerkCategory
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='/members/sign_in/')
def index(request, category=None):
    if category is not None:
        category = get_object_or_404(PerkCategory, slug=category)
        perk_list = Perk.objects.filter(category=category)
    else:
        perk_list = Perk.objects.all()
    paginator = Paginator(perk_list, 12)
    page = request.GET.get('page')
    try:
        perks = paginator.page(page)
    except PageNotAnInteger:
        perks = paginator.page(1)
    except EmptyPage:
        perks = paginator.page(paginator.num_pages)
    categories = PerkCategory.objects.all()
    return render(request, 'perks/index.html',
                  {'perks': perks, 'categories': categories,
                   'active_category': category})


class perk_detail(DetailView):

    model = Perk
