# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0021_auto_20170717_0939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='vehicle',
            new_name='vehiclescore',
        ),
    ]
