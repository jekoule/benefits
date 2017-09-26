# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perk',
            name='title',
            field=models.CharField(default='title', max_length=200, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perk',
            name='short_description',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
    ]