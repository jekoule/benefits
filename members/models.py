# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from customers.models import Company


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='Учетная запись')
    company = models.ForeignKey(Company,
                                verbose_name='Компания',
                                related_name='members')
    first_name = models.CharField(max_length=100, verbose_name='Имя',
                                  blank=True, null=True)
    last_name = models.CharField(max_length=200, verbose_name='Фамилия',
                                 blank=True, null=True)
    phone_number = models.CharField(max_length=20,
                                    verbose_name='Номер телефона',
                                    blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения',
                                     blank=True, null=True)
    activation_token = models.CharField(max_length=200, verbose_name='Токен',
                                        editable=False)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __unicode__(self):
        return self.user.email

    @property
    def email(self):
        return self.user.email

    def activate(self):
        self.user.is_active = True

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def is_admin(self):
        if self.company.admin == self.user:
            return True
        else:
            return False
