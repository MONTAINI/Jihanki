# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-23 04:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jihanki', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='age',
            field=models.CharField(max_length=100, verbose_name='年齢'),
        ),
    ]
