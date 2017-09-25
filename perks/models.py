# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from partners.models import Partner


class PerkCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __unicode__(self):
        return self.name


class Perk(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True,
                                blank=True, related_name='perks',
                                verbose_name='Партнер')
    category = models.ForeignKey(PerkCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='perks',
                                 verbose_name='Категория')
    short_description = models.CharField(max_length=200,
                                         verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание',
                                        null=True, blank=True)
    date_created = models.DateTimeField(null=True, blank=True,
                                        auto_now_add=True,
                                        verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Привилегия'
        verbose_name_plural = 'Привилегии'

    def __unicode__(self):
        return self.short_description


class PerkImage(models.Model):
    perk = models.ForeignKey(Perk, on_delete=models.CASCADE,
                             related_name='images')
    img = models.ImageField(upload_to='perks/', verbose_name='Файл')

    def thumbnail(self):
        return u'<img src="%s" width=100 height=100 />' % (self.img.url)

    thumbnail.short_description = 'Предпросмотр'
    thumbnail.allow_tags = True

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __unicode__(self):
        return self.img.url
