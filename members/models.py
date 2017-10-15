# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from customers.models import Company

phone_validator = RegexValidator(r"^[0-9]{10}$")


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='Учетная запись')
    company = models.ForeignKey(Company,
                                verbose_name='Компания',
                                related_name='members')
    first_name = models.CharField(max_length=100, verbose_name='Имя',
                                  null=True)
    last_name = models.CharField(max_length=200, verbose_name='Фамилия',
                                 null=True)
    phone_number = models.CharField(max_length=20,
                                    verbose_name='Номер телефона',
                                    null=True,
                                    validators=[phone_validator])
    date_of_birth = models.DateField(verbose_name='Дата рождения',
                                     null=True)
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
        user = self.user
        user.is_active = True
        user.save()

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def is_admin(self):
        return self.company.admin == self.user
