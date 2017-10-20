# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Bank(models.Model):
	name=models.CharField(max_length=200)
	phone=models.CharField(max_length=200)
	email=models.EmailField(max_length=200)
	logo=models.ImageField(max_length=200, help_text='require a 100 by 100 img size', upload_to='logos/')
	city=models.CharField(max_length=100)
	state=models.CharField(max_length=100)
	country=models.CharField(max_length=200)
	street=models.CharField(max_length=200)
	description=models.CharField(max_length=200)
	zip=models.CharField(max_length=50)
	license_no=models.CharField(max_length=50, default='603K498')
	website=models.URLField(default='http://www.zenithbank.com')


	def __str__(self):
		return self.name


class Product(models.Model):
	company=models.ForeignKey(Bank)
	rate=models.DecimalField(max_digits=5, decimal_places=2)
	tenure=models.IntegerField()
	max_price=models.IntegerField(default=100000000)
	min_price=models.IntegerField(default=1000000)
	processing_fee=models.IntegerField(default=10000)










