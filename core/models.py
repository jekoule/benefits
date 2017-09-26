# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='E-mail')
    date_registered = models.DateTimeField(auto_now_add=True,
                                           verbose_name='Зарегистрирован')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активен')
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Статус персонала')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Учетная запись'
        verbose_name_plural = 'Учетные записи'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    @property
    def is_member(self):
        try:
            self.member
        except ObjectDoesNotExist:
            return False
        else:
            return True

    @property
    def is_company_admin(self):
        try:
            self.member
        except ObjectDoesNotExist:
            return False
        else:
            return self.member.is_admin

    @property
    def is_partner(self):
        try:
            self.partner
        except ObjectDoesNotExist:
            return False
        else:
            return True
