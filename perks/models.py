# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import string
from django.utils.crypto import get_random_string
from django.db import models
from partners.models import Partner
from tinymce.models import HTMLField
from members.models import Member
from django.core.exceptions import ObjectDoesNotExist


class PerkCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(max_length=50, verbose_name='SLUG')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('perks.index', (), {'category': self.slug})


class Perk(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True,
                                blank=True, related_name='perks',
                                verbose_name='Партнер')
    category = models.ForeignKey(PerkCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='perks',
                                 verbose_name='Категория')
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_description = models.CharField(max_length=200,
                                         verbose_name='Краткое описание',
                                         blank=True, null=True)
    full_description = HTMLField(verbose_name='Полное описание',
                                 null=True, blank=True)
    contact_info = HTMLField(verbose_name='Контактная информация',
                             null=True, blank=True)
    date_created = models.DateTimeField(null=True, blank=True,
                                        auto_now_add=True,
                                        verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Привилегия'
        verbose_name_plural = 'Привилегии'

    def __unicode__(self):
        return self.short_description

    @property
    def thumbnail(self):
        return self.images.first().img.url

    @models.permalink
    def get_absolute_url(self):
        return ('perks.perk_detail', (), {'pk': self.pk})


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


def generate_code():
    allowed_chars = string.ascii_uppercase.replace("O", "") + string.digits
    while True:
        code = get_random_string(length=4, allowed_chars=allowed_chars)
        try:
            Transaction.objects.get(code=code)
        except ObjectDoesNotExist:
            return code


class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,
                               related_name='transcations')
    perk = models.ForeignKey(Perk, on_delete=models.DO_NOTHING,
                             related_name='transacctions')
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Дата и время')
    code = models.CharField(max_length=4,
                            default=generate_code,
                            verbose_name='Код транзакции')
