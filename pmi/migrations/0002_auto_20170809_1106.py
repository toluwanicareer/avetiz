# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-09 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='license_no',
            field=models.CharField(default='603K498', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='max_price',
            field=models.IntegerField(default=100000000),
        ),
        migrations.AddField(
            model_name='product',
            name='min_price',
            field=models.IntegerField(default=1000000),
        ),
    ]
