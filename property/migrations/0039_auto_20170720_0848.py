# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0038_property_lotsize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='value',
            field=models.IntegerField(default='1000000'),
        ),
    ]
