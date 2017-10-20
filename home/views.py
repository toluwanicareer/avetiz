# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import queryForm, pmiForm
from property.models import Property
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from property.forms import topForm
import pdb

def home(request):
	searchForm=queryForm()
	pmiform=pmiForm()
	return render(request,'home/index.html',{'searchform':searchForm,'pmiform':pmiform})

def getFeature(request):
	data=dict()
	location=request.GET.get('location')
	if location == None:
		location='FCT'
	properties=Property.objects.filter(Q(state__icontains=location),feature=True)
	if properties.count() < 3:
		properties=Property.objects.filter(Q(state__icontains=location)|Q(state__icontains='FCT'), feature=True)[:6]
	latest=Property.objects.filter(state__icontains=location).order_by('uploadDate')[:8]
	#pdb.set_trace()
	if latest.count() < 4:
		latest=Property.objects.filter(Q(state__icontains=location)|Q(state__icontains='FCT')).order_by('uploadDate','-state')[:8]
	context={'location':location, 'properties':properties, 'latest':latest, 'state':location}
	data['featurelatest']=render_to_string('home/includes/partial_feature.html', context)
	return JsonResponse(data)

def recent(request):
	location=request.GET.get('location')
	if location == None:
		location='abuja'
	latest=Property.objects.filter(Q(state__icontains=location)|Q(state__icontains='FCT')).order_by('uploadDate','-state')
	context={'latest':latest,'topform':topForm()}
	return render(request,'home/recent-listing.html', context)








