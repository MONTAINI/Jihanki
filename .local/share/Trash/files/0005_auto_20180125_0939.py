# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-25 00:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jihanki', '0004_earnings_jan_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='earnings',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created time'),
        ),
        migrations.AddField(
            model_name='loading',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created time'),
        ),
    ]
