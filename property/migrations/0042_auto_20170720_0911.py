# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0041_auto_20170720_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='area',
            field=models.IntegerField(default=5000),
        ),
    ]