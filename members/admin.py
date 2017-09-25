# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    readonly_fields = ('is_active', 'is_admin', 'activation_token')

    def is_active(self, object):
        return object.is_active

    is_active.boolean = True
    is_active.short_description = 'Активирован'

    def is_admin(self, object):
        return object.is_admin

    is_admin.short_description = 'Является администратором'
    is_admin.boolean = True


admin.site.register(Member, MemberAdmin)
