# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-08 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_property_street'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='feature',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='uploadDate',
            field=models.DateField(auto_now=True),
        ),
    ]
