# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Partner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='Учетная запись')
    name = models.CharField(max_length=100,
                            verbose_name='Наименование Компании')
    info = models.TextField(verbose_name='Контактная информация',
                            null=True, blank=True)

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'

    def __str__(self):
        return self.name
