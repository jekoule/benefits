# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import SigninForm
from perks.models import Perk, Transaction


def is_partner(user):
    if user.is_anonymous:
        return False
    else:
        return user.is_partner


def sign_in(request):
    if request.user.is_authenticated and request.user.is_partner:
        return redirect('partners:dashboard')
    next_page = request.GET.get('next')
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            login(request, user)
            if next_page is not None:
                return redirect(next_page)
            else:
                return redirect('partners:dashboard')
    else:
        form = SigninForm
    return render(request, 'partners/sign_in.html', {'form': form})


@user_passes_test(is_partner, login_url='partners:sign_in')
def dashboard(request):
    partner = request.user.partner
    transactions = Transaction.objects.filter(perk__partner=partner).order_by('-date_created')
    return render(request, 'partners/dashboard.html',
                  {'partner': partner, 'transactions': transactions})


@user_passes_test(is_partner, login_url='partners:sign_in')
def my_perks(request):
    partner = request.user.partner
    perks = Perk.objects.filter(partner=request.user.partner)
    transactions_count = Transaction.objects.filter(perk__partner=partner).order_by('-date_created').count()
    return render(request, 'partners/my_perks.html',
                  {'perks': perks, 'transactions_count': transactions_count})


@user_passes_test(is_partner, login_url='partners:sign_in')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Пароль успешно изменен',
                             extra_tags='alert-success')
            return redirect('partners:change_password')
        else:
            messages.error(request,
                           'Ошибка. Пожалуйста, \
                           проверьте введённую информацию.',
                           extra_tags='alert-danger')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'partners/change_password.html', {
        'form': form
    })
