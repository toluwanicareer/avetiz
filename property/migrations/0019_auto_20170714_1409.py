# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0018_auto_20170714_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='built',
            field=models.CharField(default='2000', max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='community',
            field=models.CharField(default='Rural Tract', max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='style',
            field=models.CharField(default='Traditional Style', max_length=200),
        ),
    ]