# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-05 00:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200605_0347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2020, 6, 5, 3, 59, 22, 106060), verbose_name='Опубликована'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2020, 6, 5, 3, 59, 22, 108053), verbose_name='Дата'),
        ),
    ]
