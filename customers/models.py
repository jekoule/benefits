# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Company(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 verbose_name='Администратор')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    address = models.CharField(max_length=200, verbose_name='Адрес',
                               blank=True, null=True)
    logo = models.ImageField(upload_to='customers/logos',
                             verbose_name='Логотип',
                             blank=True, null=True)

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name

    def total_members_count(self):
        return self.members.count()
    total_members_count.short_description = 'Количество сотрудников'

    @property
    def active_members_count(self):
        return self.members.filter(enabled=True, user__is_active=True).count()

    @property
    def pending_registration_count(self):
        return self.members.filter(user__is_active=False).count()

    @property
    def transactions_count(self):
        return sum([n.transactions_count for n in self.members.all()])
