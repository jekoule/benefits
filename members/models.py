# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import hashlib
import random
from django.core.validators import RegexValidator
from django.urls import reverse
import sendgrid
from sendgrid.helpers.mail import Mail, Email, Personalization, Substitution
from customers.models import Company

sg = sendgrid.SendGridAPIClient(
    apikey=settings.SENDGRID_API_KEY
)
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

    def generate_token(self):
        # Generating activation key
        # First generate random part as a result of hashing random string
        random_part = hashlib.sha256(str(random.random())).hexdigest()[:5]
        hashable = random_part + self.user.email.encode('utf-8')
        # Then create hash for random_part and email
        self.activation_token = hashlib.sha256(hashable).hexdigest()
        self.save()

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

    def notify_activation(self):
        mail = Mail()
        mail.from_email = Email('info@benefits.kz')
        personalization = Personalization()
        personalization.add_to(Email('o.arystanov@gmail.com'))
        #personalization.add_to(Email(self.user.email))
        activation_link = 'http://127.0.0.1:8000' + \
            reverse('members:activate') + \
            '?pk={pk}&token={token}'.format(
                pk=self.pk, token=self.activation_token
            )
        personalization.add_substitution(
            Substitution('%activation_link%', activation_link)
        )
        mail.add_personalization(personalization)
        mail.template_id = settings.SENDGRID_TEMPLATES['activation']
        sg.client.mail.send.post(request_body=mail.get())

    def notify_registration_complete(self):
        mail = Mail()
        mail.from_email = Email('info@benefits.kz')
        personalization = Personalization()
        personalization.add_to(Email('o.arystanov@gmail.com'))
        #personalization.add_to(Email(self.user.email))
        mail.add_personalization(personalization)
        mail.template_id = settings.SENDGRID_TEMPLATES['registration_complete']
        sg.client.mail.send.post(request_body=mail.get())
