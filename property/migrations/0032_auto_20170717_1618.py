# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 15:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0031_history'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='proeprty',
            new_name='property',
        ),
    ]
