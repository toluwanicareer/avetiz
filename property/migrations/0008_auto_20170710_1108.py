# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_auto_20170710_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='bed',
            field=models.CharField(default='2', max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='property',
            name='bathroom',
            field=models.CharField(default='2', max_length=200),
        ),
    ]
