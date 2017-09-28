# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Member
from .forms import SigninForm, MemberChangeForm, MemberRegisterForm


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('perks.index')
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_member:
                login(request, user)
                return redirect('perks.index')
            else:
                error = 'Вы ввели неправильное имя пользователя или пароль'
                return render(request, 'members/sign_in.html',
                              {'form': form, 'error': error})
    else:
        form = SigninForm
        return render(request, 'members/sign_in.html', {'form': form})


def register(request, pk=None, token=None):
    try:
        member = Member.objects.get(pk=pk, activation_token=token)
    except Member.DoesNotExist:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = MemberRegisterForm(request.POST, instance=member)
            if form.is_valid():
                form.save()
                member.user.set_password(form.cleaned_data['password'])
                member.activate()
                return redirect('members.success')
            else:
                messages.error(request,
                               'Ошибка. Пожалуйста, \
                               проверьте введённую информацию.',
                               extra_tags='alert-danger')
        form = MemberRegisterForm()
        return render(request, 'members/register.html', {'form': form})


def edit_info(request):
    member = request.user.member
    if request.method == 'POST':
        form = MemberChangeForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация успешно обновлена',
                             extra_tags='alert-success')
            return redirect('members.edit_info')
        else:
            messages.error(request,
                           'Ошибка. Пожалуйста, \
                           проверьте введённую информацию.',
                           extra_tags='alert-danger')
    else:
        form = MemberChangeForm(instance=member)
    return render(request, 'members/edit_info.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Пароль успешно изменен',
                             extra_tags='alert-success')
            return redirect('members.change_password')
        else:
            messages.error(request,
                           'Ошибка. Пожалуйста, \
                           проверьте введённую информацию.',
                           extra_tags='alert-danger')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'members/change_password.html', {
        'form': form
    })


def my_perks(request):
    transactions = request.user.member.transactions.all()
    return render(request, 'members/my_perks.html',
                  {'transactions': transactions})
