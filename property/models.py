# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .choices import *

from django.db import models
from .choices import *
from django.db.models.signals import post_save
from django.dispatch import receiver
import pdb
# Create your models here.

class Developer(models.Model):
	name=models.CharField(max_length=20)
	website=models.URLField(max_length=200)
	address=models.CharField(max_length=20)
	
	def __str__(self):
		return self.name

class Feature(models.Model):
	name=models.CharField(max_length=20)
	category=models.CharField(max_length=20, choices=FEATURE_CATEGORY_CHOICES, default='')
	header=models.CharField(max_length=20, default='')
	
	def __str__(self):
		return self.name


class Property(models.Model):
	title=models.CharField(max_length=200)
	street=models.CharField(max_length=200, default='No 16 Lugbe Federal housing')
	city=models.CharField(max_length=200)
	state=models.CharField(max_length=200)
	Country=models.CharField(max_length=200, default='nigeria')
	types=models.CharField(max_length=200, choices=TYPE_CHOICES,default='Land')
	status=models.CharField(max_length=200, choices=STATUS_CHOICES, default='sale')
	bedroom=models.IntegerField(default='2')
	bathroom=models.IntegerField(default='3')
	value=models.IntegerField(default=1000000, help_text='Naira value of the property')
	area=models.IntegerField(default=5000)
	feature=models.BooleanField(default=False)
	uploadDate=models.DateField(auto_now=True)
	latitude=models.CharField(max_length=200, default='')
	longitude=models.CharField(max_length=200, default='')
	developer=models.ForeignKey(Developer, on_delete=models.CASCADE,default='')
	zipcode=models.CharField(max_length=200, default='234')
	actual_value=models.CharField(max_length=200, default='500000')
	discount=models.CharField(max_length=200, default='0.1')
	features=models.ManyToManyField(Feature, default='')
	bathroom=models.CharField(max_length=200, default='2')
	description=models.TextField(default='"oriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate "')
	thumbnail=models.TextField(default='http://mallorcapropertyhouse.co.uk/wp-content/uploads/2014/10/Beautiful_Luxury_House_with_Swiming_Pool_Wallpapers_for_Desktop.jpg')
	projection=models.CharField(max_length=200,default='3.4')
	community=models.CharField(max_length=200,default='Rural Tract')
	style=models.CharField(max_length=200,default="Traditional Style")
	built=models.CharField(max_length=200, default='2000')
	stories=models.CharField(max_length=200,default='5')
	walkscore=models.IntegerField(default='4')
	trainscore=models.IntegerField(default='0')
	vehiclescore=models.IntegerField(default='8')
	transdesc=models.TextField(default='Lorem Ipsum is simply dummy text of the printing and typesetting industry.')
	lotsize=models.CharField(max_length=50, default='45 x 107')
	refernceid=models.CharField(max_length=200, null=True, blank=True)
	agentname=models.CharField(max_length=100, default="Funmi Ajayi")
	dollarprice=models.IntegerField(null=True, blank=True)


	def __str__(self):
		return  self.title + ' ' + self.state


	

class Picture(models.Model):
	src=models.CharField(max_length=200)
	property=models.ForeignKey(Property)
	featured=models.BooleanField(default=False)
	type=models.CharField(max_length=200, choices=PICTURE_TYPE_CHOICES)

	def __str__(self):
		return self.property.title
	
class Sale(models.Model):
	property=models.OneToOneField(Property)
	date=models.DateField(null=True, blank=True)	
	buyer=models.CharField(max_length=100)
	completion_state=models.CharField(max_length=100, choices=PAYMENT_STATE_CHOICES)
	bought_at=models.IntegerField()
	down_payt=models.IntegerField(default=200000)
	state=models.CharField(default='True', choices=(('True','True'),('false','False')), max_length=10)
	pptystate=models.CharField(max_length=100, default="lagos")

class Offer(models.Model):
	property=models.ForeignKey(Property)
	offerprice=models.IntegerField()
	buyer=models.CharField(max_length=100)

class History(models.Model):
	property=models.ForeignKey(Property)
	changefrom=models.IntegerField(default=1000000)
	changeto=models.IntegerField(default=2000000)
	date=models.DateField()
	source=models.CharField(max_length=200)

class Bathroom(models.Model):
	property=models.OneToOneField(Property, related_name='house')
	noofbath=models.IntegerField()

class Kitchen(models.Model):
	property=models.OneToOneField(Property)
	noofkitchen=models.IntegerField()
	noofstove=models.IntegerField()
	eat=models.BooleanField()

class Equipment(models.Model):
	property=models.ForeignKey(Property)
	count=models.IntegerField()
	name=models.CharField(max_length=50)

class Cooling(models.Model):
	property=models.OneToOneField(Property)
	waterheater=models.BooleanField()
	ac=models.BooleanField()

class Room(models.Model):
	property=models.OneToOneField(Property)
	count=models.IntegerField()
	familyrooms=models.IntegerField()
	diningroom=models.BooleanField()
	diningnumber=models.IntegerField()

class Building(models.Model):
	property=models.OneToOneField(Property)
	construction=models.CharField(max_length=200)

class Exterior(models.Model):
	property=models.OneToOneField(Property)
	apperance=models.CharField(max_length=100 )
	deck=models.CharField(max_length=10,choices=(('True','true'),('False','false')))


class  Level(models.Model):
	property=models.ForeignKey(Property, null=True)
	feature=models.CharField(max_length=100)
	number=models.IntegerField()

class Parking(models.Model):
	property=models.OneToOneField(Property, null=True)
	garagecount=models.IntegerField()
	garagetype=models.CharField(max_length=100, blank=True)

class Schools(models.Model):
	property=models.ForeignKey(Property)
	name=models.CharField(max_length=100)

class Utility(models.Model):
	property=models.ForeignKey(Property)
	name=models.CharField(max_length=100)

class places(models.Model):
	city=models.CharField(max_length=100)
	transdesc=models.TextField()

class Tour(models.Model):
	tourdate=models.DateField()
	property=models.ForeignKey(Property)
	name=models.CharField(max_length=50)

@receiver(post_save, sender=Property)
def my_callback(sender, instance, *args, **kwargs):
    #instance.slug = slugify(instance.title)
    city=instance.city[:3]
    country=instance.Country[:3]
    state=instance.state[:3]
    ids=instance.id
    #pdb.set_trace()
    property=Property.objects.filter(id=instance.id)
    newrefernceid=country+state+city+str(ids)
    newrefernceid=newrefernceid.upper()
    #pdb.set_trace()
    property.update(refernceid=newrefernceid)


