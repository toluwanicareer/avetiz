# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 08:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0009_auto_20170720_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='help',
            name='cat',
        ),
    ]
