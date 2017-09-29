# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Perk, PerkCategory, Transaction


@login_required(login_url='/account/sign_in/')
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


@login_required(login_url='/account/sign_in/')
def perk_detail(request, pk):
    perk = get_object_or_404(Perk, pk=pk)
    if request.method == 'POST':
        transaction = Transaction(member=request.user.member,
                                  perk=perk)
        transaction.save()
        subject, from_email = 'Код', 'info@benefits.kz'
        to_email = [request.user.email]
        text = 'Ваш код транзакции: %s' % transaction.code
        send_mail(subject, text, from_email, to_email)
        messages.success(request, transaction.code)
    return render(request, 'perks/perk_detail.html', {'perk': perk})
