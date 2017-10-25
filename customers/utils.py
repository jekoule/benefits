# -*- coding: utf-8 -*-
import csv
import re
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib import messages
from members.models import Member
User = get_user_model()


def create_member(email, company):
    # Create user account for member with random password
    user = User(email=email, is_active=False)
    password = User.objects.make_random_password()
    user.set_password(password)
    user.save()
    member = Member(user=user, company=company)
    member.save()
    member.generate_token()
    # Finally send an email to member with an invitation to activate account
    member.notify_activation()


def create_member_multiple(request, emails, company):
    EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    success = 0
    for email in emails:
        if email != '':
            if EMAIL_REGEX.match(email):
                try:
                    create_member(email, company)
                except IntegrityError:
                    messages.error(request,
                                   ('Не удалось добавить {email}. Пользователь \
                                   с таким адресом уже существует').format(email=email),
                                   extra_tags='text-danger')
                else:
                    success += 1
            else:
                messages.error(request,
                               ('Не удалось добавить {email}. Проверьте \
                                правильность данного email-адреса.').format(email=email),
                               extra_tags='text-danger')
    if success > 0:
        messages.success(request, ('Успешно добавлено {n} сотрудников.').format(n=success),
                         extra_tags='text-success')


def create_members_from_list(request, list, company):
    emails = list.split()
    create_member_multiple(request, emails, company)


def create_members_from_file(request, file, company):
    reader = csv.reader(file)
    emails = [row[0] for row in reader]
    create_member_multiple(request, emails, company)
