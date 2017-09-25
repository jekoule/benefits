# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Perk, PerkImage, PerkCategory


class ImageInline(admin.TabularInline):
    model = PerkImage
    fields = ('perk', 'img', 'thumbnail',)
    readonly_fields = ('thumbnail', )
    extra = 1


class PerkAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


admin.site.register(Perk, PerkAdmin)
admin.site.register(PerkCategory)
