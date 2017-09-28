# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Perk, PerkImage, PerkCategory, Transaction


class ImageInline(admin.TabularInline):
    model = PerkImage
    fields = ('perk', 'img', 'thumbnail',)
    readonly_fields = ('thumbnail', )
    extra = 1


class PerkAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('member', 'perk', 'date_created', 'code')


admin.site.register(Perk, PerkAdmin)
admin.site.register(PerkCategory, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
