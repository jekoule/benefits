# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Member
from .forms import EditForm, RegisterForm, SigninForm


def is_member(user):
    if user.is_anonymous:
        return False
    else:
        return user.is_member


def sign_in(request):
    if request.user.is_authenticated and request.user.is_member:
        return redirect('perks:index')
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
                return redirect('perks:index')
    else:
        form = SigninForm
    return render(request, 'members/sign_in.html', {'form': form})


def activate(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        token = str(request.GET.get('token'))
        try:
            member = Member.objects.get(pk=pk, activation_token=token)
            if member is not None:
                if member.is_active:
                    return redirect('perks:index')
                else:
                    login(request, member.user)
                    return redirect('members:register')
        except ObjectDoesNotExist:
            pass
    return HttpResponseForbidden()


@login_required(login_url='members:sign_in')
def register(request):
    if request.method == 'POST':
        member = request.user.member
        form = RegisterForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            member.user.set_password(form.cleaned_data['password'])
            member.activate()
            login(request, member.user)
            return redirect('members:success')
        else:
            messages.error(request,
                            'Ошибка. Пожалуйста, \
                            проверьте введённую информацию.',
                            extra_tags='alert-danger')
    form = RegisterForm()
    return render(request, 'members/register.html', {'form': form})


class registration_success(TemplateView):
    template_name = 'members/registration_success.html'


@user_passes_test(is_member, login_url='members:sign_in')
@user_passes_test(lambda user: user.is_active, login_url='members:register')
def edit_info(request):
    member = request.user.member
    if request.method == 'POST':
        form = EditForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация успешно обновлена',
                             extra_tags='alert-success')
            return redirect('members:edit_info')
        else:
            messages.error(request,
                           'Ошибка. Пожалуйста, \
                           проверьте введённую информацию.',
                           extra_tags='alert-danger')
    else:
        form = EditForm(instance=member)
    return render(request, 'members/edit_info.html', {'form': form})


@user_passes_test(is_member, login_url='members:sign_in')
@user_passes_test(lambda user: user.is_active, login_url='members:register')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Пароль успешно изменен',
                             extra_tags='alert-success')
            return redirect('members:change_password')
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


@user_passes_test(is_member, login_url='members:sign_in')
@user_passes_test(lambda user: user.is_active, login_url='members:register')
def my_perks(request):
    transactions = request.user.member.transactions.order_by('-date_created')
    return render(request, 'members/my_perks.html',
                  {'transactions': transactions})
