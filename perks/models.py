# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import string
from django.utils.crypto import get_random_string
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.conf import settings
from geoposition.fields import GeopositionField
import sendgrid
from sendgrid.helpers.mail import Mail, Email, Personalization, Substitution
import urllib.request as urllib

from partners.models import Partner
from tinymce.models import HTMLField
from members.models import Member

sg = sendgrid.SendGridAPIClient(
    apikey=settings.SENDGRID_API_KEY
)


class PerkCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(max_length=50, verbose_name='SLUG')
    icon = models.FileField(upload_to='category_icons/',
                            verbose_name='SVG иконка',
                            blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def render_icon(self):
        if self.icon:
            return mark_safe(self.icon.read())

    @models.permalink
    def get_absolute_url(self):
        return ('perks:category', (), {'category': self.slug})


class Perk(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True,
                                blank=True, related_name='perks',
                                verbose_name='Партнер')
    category = models.ForeignKey(PerkCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='perks',
                                 verbose_name='Категория')
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    discount = models.CharField(max_length=200, verbose_name='Скидка',
                                blank=True, null=True)
    short_description = models.CharField(max_length=200,
                                         verbose_name='Краткое описание',
                                         blank=True, null=True)
    full_description = HTMLField(verbose_name='Полное описание',
                                 null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='Адрес',
                               null=True, blank=True)
    phone_number = models.CharField(max_length=200, verbose_name='Телефон',
                                    null=True, blank=True)
    website = models.URLField(verbose_name='Веб-сайт', null=True, blank=True)
    geoposition = GeopositionField(verbose_name='Геолокация',
                                   null=True, blank=True)
    active = models.BooleanField(default=True,
                                 verbose_name='Предложение активно')
    date_created = models.DateTimeField(null=True, blank=True,
                                        auto_now_add=True,
                                        verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Предложения'
        verbose_name_plural = 'Предложения'

    def __str__(self):
        return self.title

    @property
    def thumbnail(self):
        if self.images.first():
            return self.images.first().img.url

    @models.permalink
    def get_absolute_url(self):
        return ('perks:perk_detail', (), {'pk': self.pk})

    @models.permalink
    def get_modal_url(self):
        return ('perks:perk_modal', (), {'pk': self.pk})

    @models.permalink
    def get_perk_url(self):
        return ('perks:get_perk', (), {'pk': self.pk})

    def partner_name(self):
        return self.partner.name
    partner_name.short_description = 'Партнер'


class PerkImage(models.Model):
    perk = models.ForeignKey(Perk, on_delete=models.CASCADE,
                             related_name='images')
    img = models.ImageField(upload_to='perks/', verbose_name='Файл')

    def thumbnail(self):
        return u'<img src="%s" width=100 height=100 />' % (self.img.url)

    thumbnail.short_description = 'Предпросмотр'
    thumbnail.allow_tags = True

    class Meta:
        verbose_name = 'картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
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
                               related_name='transactions',
                               verbose_name='Сотрудник')
    perk = models.ForeignKey(Perk, on_delete=models.DO_NOTHING,
                             related_name='transactions',
                             verbose_name='Предложение')
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Дата и время')
    code = models.CharField(max_length=4,
                            default=generate_code,
                            verbose_name='Код транзакции')

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return self.code

    def notify_member(self):
        mail = Mail()
        mail.from_email = Email('info@benefits.kz')
        personalization = Personalization()
        personalization.add_to(Email('o.arystanov@gmail.com'))
        #personalization.add_to(Email(self.member.user.email))
        mail.add_personalization(personalization)
        mail.template_id = settings.SENDGRID_TEMPLATES['activation']
        try:
            response = sg.client.mail.send.post(request_body=mail.get())
        except urllib.HTTPError as e:
            print(e.read())
            exit()
        print(response.status_code)
        print(response.body)
        print(response.headers)
