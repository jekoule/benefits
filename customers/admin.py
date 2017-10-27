# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Company
from members.models import Member


class MemberInline(admin.TabularInline):
    model = Member
    readonly_fields = ('user', 'first_name', 'last_name',
                       'phone_number', 'date_of_birth')
    extra = 0
    can_delete = False

    def has_add_permission(self, request):
        return False


class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('total_members_count', 'active_members_count',
                       'transactions_count',)
    inlines = (MemberInline,)


admin.site.register(Company, CompanyAdmin)
