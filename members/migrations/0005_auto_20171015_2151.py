# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 15:51
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20171015_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone_number',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator('^+[0-9]{10}+$')], verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430'),
        ),
    ]
