# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView

from .models import Perk, PerkCategory, Transaction
from members.views import is_member


def index(request, category=None):
    if category is not None:
        category = get_object_or_404(PerkCategory, slug=category)
        perk_list = Perk.objects.filter(category=category, active=True)
    else:
        perk_list = Perk.objects.filter(active=True)
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


@user_passes_test(is_member, login_url='members:sign_in')
@user_passes_test(lambda user: user.is_active, login_url='members:register')
def perk_modal(request, pk):
    perk = get_object_or_404(Perk, pk=pk)
    return render(request, 'perks/partials/modal.html', {'perk': perk})


@user_passes_test(is_member, login_url='members:sign_in')
@user_passes_test(lambda user: user.is_active, login_url='members:register')
def get_perk(request, pk):
    perk = get_object_or_404(Perk, pk=pk)
    transaction = Transaction(member=request.user.member,
                              perk=perk)
    transaction.save()
    subject, from_email = 'Код', 'info@benefits.kz'
    to_email = [request.user.email]
    text = 'Ваш код транзакции: %s' % transaction.code
    send_mail(subject, text, from_email, to_email)
    return render(request, 'perks/result.html',
                  {'transaction_code': transaction.code})
