# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0019_auto_20170714_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='stories',
            field=models.CharField(default='5', max_length=200),
        ),
    ]
