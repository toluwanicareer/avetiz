# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 08:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0050_auto_20170724_0904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='bed',
        ),
    ]