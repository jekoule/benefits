# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from members.models import Member
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .utils import create_members_from_list, create_members_from_file


def is_admin(user):
    if user.is_anonymous:
        return False
    else:
        return user.is_company_admin


@user_passes_test(is_admin, login_url='members:sign_in')
def dashboard(request):
    company = request.user.member.company
    return render(request, 'customers/dashboard.html', {'company': company})


@user_passes_test(is_admin, login_url='members:sign_in')
def delete_members(request):
    if request.method == 'POST':
        to_delete = request.POST.getlist('to_delete')
        for member_pk in to_delete:
            try:
                member = Member.objects.get(pk=member_pk)
            except ObjectDoesNotExist:
                pass
            else:
                member.user.delete()
                # delete User & Member instance
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(is_admin, login_url='members:sign_in')
def add_members(request):
    if request.method == 'POST':
        company = request.user.member.company
        if 'members_list' in request.POST:
            create_members_from_list(request,
                                     request.POST.get('members_list'), company)
        elif 'members_file' in request.FILES:
            create_members_from_file(request,
                                     request.FILES['members_file'], company)
        return redirect('customers:dashboard')
    return render(request, 'customers/add_members.html')
