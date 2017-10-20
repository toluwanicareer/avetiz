# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Help(models.Model):
	title=models.CharField(max_length=200)
	answer=models.TextField()
	#cat=models.CharField(max_length=200, default='buyer')
	#main=models.BooleanField(default=False)
	
	def __str__(self):
		return self.title



	
		
	
	
	
	
