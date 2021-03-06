# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 14:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441')),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u0410\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f',
                'verbose_name_plural': '\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u0438',
            },
        ),
    ]
