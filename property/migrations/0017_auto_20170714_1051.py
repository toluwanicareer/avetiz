# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0016_property_projection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='value',
            field=models.IntegerField(default='1000000', max_length=200),
        ),
    ]
