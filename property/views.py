# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from django.db.models import Avg,Count
from django.core.exceptions import ObjectDoesNotExist
from home.forms import queryForm
from django.core import serializers
from avetiz import settings
import pdb
import math
from datetime import date


def listProperty(request):
	if request.method == 'POST':
		form = SortForm(request.POST)	
		if form.is_valid():
			order= form.cleaned_data['order_by_column']
			limit=form.cleaned_data['limit']
			property=Property.objects.all().order_by(order)
			paginator = Paginator(property, limit) # Show limit property per page
			page = request.GET.get('page')
			try:
				listing= paginator.page(page)
			except PageNotAnInteger:
				listing = paginator.page(1)
			except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
				listing = paginator.page(paginator.num_pages)
		return render(request, 'property/property.html', {'property': listing, 'form':SortForm()})
	
	property=Property.objects.all().order_by('value')
	paginator = Paginator(property, 6) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		listing= paginator.page(page)
	except PageNotAnInteger:
		listing = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		listing = paginator.page(paginator.num_pages)
	return render(request, 'property/property.html', {'property': listing, 'form':SortForm()})

	
def searchProperty(request):	
	if not request.method=='POST':
		if 'search_parameter' in request.session:
			request.POST=request.session['search_parameter']
			request.method='POST'
		else:
			form=queryForm()
			return render(request,'home/index.html', {'searchform':form})

	if request.method=='POST':
		request.session['search_parameter']=request.POST
		#pdb.set_trace()
		if 'topform' in request.POST :
			topform=topForm(request.POST)
			if topform.is_valid():
				city=topform.cleaned_data['city']
				state=topform.cleaned_data['state']
				country=topform.cleaned_data['country']
				query=topform.cleaned_data['search']
				types=topform.cleaned_data['propertytype']
				bedno=topform.cleaned_data['bedno']
				bathno=topform.cleaned_data['bathno']
				if city:
					result=Property.objects.filter(city__icontains=city)
					result=topFormFilter(types,bedno,bathno,result)	
					if not result.exists():
						result=Property.objects.filter(state__icontains=state)
						result=topFormFilter(types,bedno,bathno,result)

					if not result.exists():
						result=Property.objects.filter(feature=True)						
						listing=getlisting(result,3,request)
						return render(request,'property/search.html',{'result':listing,'topform':topForm(),'filterform':filterForm()})	
				
				if state and not city:
					result=Property.objects.filter(state__icontains=state)
					result=topFormFilter(types,bedno,bathno,result)			
					if not result.exists():							
						result=Property.objects.filter(feature=True)						
						listing=getlisting(result,3,request)
						return render(request,'property/search.html',{'result':listing,'topform':topForm(),'filterform':filterForm()})
				
				if not state and not city:
					#pdb.set_trace()
					context=get_no_result_context(query=query,request=request,types=types,bedno=bedno,bathno=bathno)	
					#pdb.set_trace()	
					return render(request, 'property/search.html',context)
				context=getContext(city,country,state,result,request,query,types,bedno,bathno,'home')
				request.session['count']=result.count()
				request.session['query']=query
				return render(request,'property/search.html',context)

		elif 'minprice' in request.POST or 'maxprice' in request.POST:
			form=filterForm(request.POST)	
			
			return render(request,'property/search.html',context)

		elif 'hiddenquery' in request.POST and request.POST.get('hiddentypeoforder') == 'newest':
			#pdb.set_trace()
			city=request.POST.get('hiddencity')
			state=request.POST.get('hiddenstate')
			country=request.POST.get('hiddencountry')
			query=request.POST.get('hiddenquery')
			bedno=request.POST.get('hiddenbedno')
			bathno=request.POST.get('hiddenbathno')
			types=request.POST.get('hiddenpropertytype')
			try:
				resultcount=int(request.POST.get('count'))
			except:
				resultcount=0
			if city:
				result=Property.objects.filter(city__icontains=city).order_by('-uploadDate')
				if not result.exists()  or result.count != resultcount :
					result=Property.objects.filter(state__icontains=state).order_by('-uploadDate')
					if not result.exists() or result.count() != resultcount:
						result=Property.objects.filter(state__icontains=state).order_by('-uploadDate')
						if not result.exists()  or result.count() != resultcount:
							context=get_no_result_context(query=query,request=request, highlight='newest')		
							return render(request, 'property/search.html',context)
							#result=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query)).order_by('-uploadDate')
							if not result.exists():
								result=Property.objects.filter(feature=True)
								listing=getlisting(result,3,request)
								return render(request,'property/search.html',{'result':listing,'topform':topForm()})
					
			if state and not city:
				result=Property.objects.filter(state__icontains=state).order_by('-uploadDate')
				if not result.exists()  or result.count() != resultcount:
					result=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query)).order_by('-uploadDate')
					if not result.exists():
						result=Property.objects.filter(feature=True)
						listing=getlisting(result,3,request)
						return render(request,'property/search.html',{'result':listing,'topform':topForm()})
			if not state and not city:
				#pdb.set_trace()
				context=get_no_result_context(query=query,request=request, highlight='newest')		
				return render(request, 'property/search.html',context)
			#pdb.set_trace()
			context=getContext(city,country,state,result,request,query,types,bedno,bathno,'newest')
			return render(request,'property/search.html',context)

		elif 'hiddenquery' in request.POST and request.POST.get('hiddentypeoforder')=='homes':
			#pdb.set_trace()
			city=request.POST.get('hiddencity')
			state=request.POST.get('hiddenstate')
			country=request.POST.get('hiddencountry')
			query=request.POST.get('hiddenquery')
			bedno=request.POST.get('hiddenbedno')
			bathno=request.POST.get('hiddenbathno')
			types=request.POST.get('hiddenpropertytype')
			resultcount=int(request.POST.get('count'))
			#pdb.set_trace()
			if city:
				result=Property.objects.filter(city__icontains=city)
				if not result.exists()  or result.count() != resultcount :
					result=Property.objects.filter(state__icontains=state)
					if not result.exists() or result.count() != resultcount:
						result=Property.objects.filter(state__icontains=state)
						if not result.exists()  or result.count() != resultcount:
							result=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query))
							if not result.exists():
								result=Property.objects.filter(feature=True)
								listing=getlisting(result,3,request)
								return render(request,'property/search.html',{'result':listing,'topform':topForm()})
					
			if state and not city:
				result=Property.objects.filter(state__icontains=state)
				if not result.exists():
					result=Property.objects.filter(feature=True)
					listing=getlisting(result,3,request)
					return render(request,'property/search.html',{'result':listing,'topform':topForm()})
			if not state and not city:
				#pdb.set_trace()
				context=get_no_result_context(query=query,request=request)		
				return render(request, 'property/search.html',context)
			context=getContext(city,country,state,result,request,query,types,bedno,bathno,'home')
			return render(request,'property/search.html',context)

		elif 'hiddenquery' in request.POST and request.POST.get('hiddentypeoforder')=='cheap':
			city=request.POST.get('hiddencity')
			state=request.POST.get('hiddenstate')
			country=request.POST.get('hiddencountry')
			query=request.POST.get('hiddenquery')
			bedno=request.POST.get('hiddenbedno')
			bathno=request.POST.get('hiddenbathno')
			types=request.POST.get('hiddenpropertytype')
			resultcount=int(request.POST.get('count'))
			if city:
				result=Property.objects.filter(city__icontains=city).order_by('value')
				if not result.exists()  or result.count() != resultcount :
					result=Property.objects.filter(state__icontains=state).order_by('value')
					if not result.exists() or result.count() != resultcount:
						result=Property.objects.filter(state__icontains=state).order_by('value')
						if not result.exists()  or result.count() != resultcount:
							result=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query)).order_by('value')
							if not result.exists():
								result=Property.objects.filter(feature=True)
								listing=getlisting(result,3,request)
								return render(request,'property/search.html',{'result':listing,'topform':topform})
					
			if state and not city:
				result=Property.objects.filter(state__icontains=state).order_by('value')
				if not result.exists():
					result=Property.objects.filter(feature=True)
					listing=getlisting(result,3,request)
					return render(request,'property/search.html',{'result':listing,'topform':topform})
			if not state and not city:
				#pdb.set_trace()
				context=get_no_result_context(query=query,request=request)		
				return render(request, 'property/search.html',context)
			context=getContext(city,country,state,result,request,query,types,bedno,bathno,'cheap')
			return render(request,'property/search.html',context)

		elif 'hiddenquery' in request.POST and request.POST.get('onehome')=='yes':

			#pdb.set_trace()
			city=request.POST.get('hiddencity')
			state=request.POST.get('hiddenstate')
			country=request.POST.get('hiddencountry')
			query=request.POST.get('hiddenquery')
			bedno=request.POST.get('hiddenbedno')
			bathno=request.POST.get('hiddenbathno')
			types=request.POST.get('hiddenpropertytype')
			if city:
				result=Property.objects.filter(city__icontains=city).filter(bedroom=1)
				if not result.exists() or request.session['onebedroomcount'] != result.count():
					
					result=Property.objects.filter(state__icontains=state).filter(bedroom=1)
					if not result.exists() or request.session['onebedroomcount'] != result.count():
						#result=Property.objects.filter(Q(street__icontains=query)|Q(city__icontains=city)|Q(state__icontains=query)|Q(Country__icontains=query), bedroom=1)
						context=get_no_result_context(query=query,request=request)
						return render(request,'property/search.html',context)
						if not result.exists():
							result=Property.objects.filter(feature=True)
							listing=getlisting(result,3,request)
							return render(request,'property/search.html',{'result':listing,'topform':topForm()})
					
			if state and not city:
				result=Property.objects.filter(state__icontains=state).filter(bedroom=1)
				if not result.exists():
					result=Property.objects.filter(feature=True)
					listing=getlisting(result,3,request)
					return render(request,'property/search.html',{'result':listing,'topform':topForm()})
			if not state and not city:
				#pdb.set_trace()
				context=get_no_result_context(query=query,request=request)		
				return render(request, 'property/search.html',context)
			context=getContext(city,country,state,result,request,query,types,bedno,bathno,'home')
			return render(request,'property/search.html',context)


		elif 'hiddenquery' in request.POST and request.POST.get('twohome')=='yes':
			#pdb.set_trace()
			city=request.POST.get('hiddencity')
			state=request.POST.get('hiddenstate')
			country=request.POST.get('hiddencountry')
			query=request.POST.get('hiddenquery')
			bedno=request.POST.get('hiddenbedno')
			bathno=request.POST.get('hiddenbathno')
			types=request.POST.get('hiddenpropertytype')
			if city:
				result=Property.objects.filter(city__icontains=city).filter(bedroom=2)
				if not result.exists() or request.session['twobedroomcount'] != result.count():
					
					result=Property.objects.filter(state__icontains=state).filter(bedroom=2)
					if not result.exists() or request.session['twobedroomcount'] != result.count():
						result=Property.objects.filter(Q(street__icontains=query)|Q(city__icontains=city)|Q(state__icontains=query)|Q(Country__icontains=query), bedroom=2)
						if not result.exists():
							result=Property.objects.filter(feature=True)
							listing=getlisting(result,3,request)
							return render(request,'property/search.html',{'result':listing,'topform':topForm()})
					
			if state and not city:
				result=Property.objects.filter(state__icontains=state).filter(bedroom=2)
				if not result.exists():
					result=Property.objects.filter(feature=True)
					listing=getlisting(result,3,request)
					return render(request,'property/search.html',{'result':listing,'topform':topForm()})
			if not state and not city:
				#pdb.set_trace()
				context=get_no_result_context(query=query,request=request)		
				return render(request, 'property/search.html',context)
			context=getContext(city,country,state,result,request,query,types,bedno,bathno,'home')
			return render(request,'property/search.html',context)


		elif 'hiddenquery' in request.POST and request.POST.get('threehome')=='yes':
			city=request.POST.get('hiddencity')
			state=request.POST.get('hiddenstate')
			country=request.POST.get('hiddencountry')
			query=request.POST.get('hiddenquery')
			bedno=request.POST.get('hiddenbedno')
			bathno=request.POST.get('hiddenbathno')
			types=request.POST.get('hiddenpropertytype')
			if city:
				result=Property.objects.filter(city__icontains=city).filter(bedroom__gte=3)
				if not result.exists() or request.session['morebedroomcount'] != result.count():
					
					result=Property.objects.filter(state__icontains=state).filter(bedroom__gte=3)
					if not result.exists() or request.session['morebedroomcount'] != result.count():
						result=Property.objects.filter(Q(street__icontains=query)|Q(city__icontains=city)|Q(state__icontains=query)|Q(Country__icontains=query), bedroom__gte=3)
						if not result.exists():
							result=Property.objects.filter(feature=True)
							listing=getlisting(result,3,request)
							return render(request,'property/search.html',{'result':listing,'topform':topForm()})
					
			if state and not city:
				result=Property.objects.filter(state__icontains=state).filter(bedroom__gte=3)
				if not result.exists():
					result=Property.objects.filter(feature=True)
					listing=getlisting(result,3,request)
					return render(request,'property/search.html',{'result':listing,'topform':topForm()})
			if not state and not city:
				context=get_no_result_context(query=query,request=request)		
				return render(request, 'property/search.html',context)
			context=getContext(city,country,state,result,request,query,types,bedno,bathno,'home')
			return render(request,'property/search.html',context)

		else:
			form=queryForm(request.POST)
			if form.is_valid():
				topform=topForm()
				city=form.cleaned_data['city']
				state=form.cleaned_data['state']
				country=form.cleaned_data['country']
				query=form.cleaned_data['query']
				#pdb.set_trace()
				if city:
					result=Property.objects.filter(city__icontains=city)

					if not result.exists():
						result=Property.objects.filter(state__icontains=state)
						if not result.exists():
							result=Property.objects.filter(feature=True)
							listing=getlisting(result,3,request)
							return render(request,'property/search.html',{'result':listing,'topform':topform})
					
				if state and not city:
					result=Property.objects.filter(state__icontains=state)
					if not result.exists():
						result=Property.objects.filter(feature=True)
						listing=getlisting(result,3,request)
						return render(request,'property/search.html',{'result':listing,'topform':topform})
				if not state and not city:
					
					context=get_no_result_context(query=query,request=request,highlight='home')		
					return render(request, 'property/search.html',context)
				#pdb.set_trace()
				context=getContext(city,country,state,result,request,query,'','','','home')
				#pdb.set_trace()
				request.session['count']=result.count()
				request.session['query']=query
				return render(request,'property/search.html',context)


def propertyDetail(request, property_id):
	result=get_object_or_404(Property, pk=property_id)
	stateresult=Property.objects.filter(state__icontains=result.state)
	count=stateresult.count
	values=[int(property.value) for property in stateresult]
	stateaverage=Property.objects.values('state').annotate(Avg('value')).filter(state__icontains=result.state)
	mid=median(values)
	try:
		similarpptysold=Property.objects.filter(Q(sale__state__icontains='True'),state__icontains=result.state)
	except :
		try:
			similarpptysold=Property.objects.filter(Q(sale__state__icontains='True'),country__icontains=result.country)
		except :
			try:
				similarpptysold=Property.objects.filter(sale__state__icontains='True')
			except :
				similarpptysold='-'
	try:
		similarppty=Property.objects.filter(state__icontains=result.state).exclude(sale__state__icontains='True')
	except :
		try:
			similarppty=Property.objects.filter(country__icontains=result.country).exclude(sale__state__icontains='True')
		except :
			similarppty='-'
	try:
		pptysold=Sale.objects.values('state').annotate(Count('buyer')).get(pptystate__icontains=result.state)
		avgdeposit=Sale.objects.values('state').annotate(Avg('down_payt')).get(pptystate__icontains=result.state)
	except:
		pptysold='-'
		avgdeposit='-'
	try:
		avgoffer=Offer.objects.values('property').annotate(Avg('offerprice')).get(property=result)
	except :
		avgoffer='no offer yet'
	try:
		similarhomes=Property.objects.filter(city__icontains=result.city)
	except :
		try:
			similarhomes=Property.objects.filter(city__icontains=result.state)
		except  :
			similarhomes=Property.objects.filter(city__icontains=result.country)
	try:
		history=History.objects.filter(property=result)
	except :
		history='-'
	max_range=int(result.value)*1.2
	min_range=int(result.value)*0.8
	initialdownpayt=int(result.value)*0.4
	principal=(int(result.value)-initialdownpayt)/60
	request.session['state']=result.state
	request.session['city']=result.city
	request.session['country']=result.Country
	detailform=detailcontactform()
	try:
		resultcount=request.session['count']
	except KeyError:
		resultcount=0

	try:
		resultquery=request.session['query']
	except KeyError:
		resultquery=result.street



	context={
	'result':result,
	'detailform':detailform,
	'median':mid,
	'stateaverage':stateaverage,
	'count':count,
	'avgoffer':avgoffer,
	'pptysold':pptysold,
	'avgdeposit':avgdeposit,
	'similarpptysold':similarpptysold,
	'similarhomes':similarhomes,
	'history':history,
	'minrange':min_range,
	'maxrange':max_range,
	'payt':initialdownpayt,
	'principal':principal,
	'nearbycount':resultcount,
	'nearbyquery':resultquery,
	'topform':topForm(),
	'detailtopform':detailContactFormTop(),
	}

	return render(request,'property/detail.html',context)


def median(lst):
	    lst = sorted(lst)
	    n = len(lst)
	    if n < 1:
	            return None
	    if n % 2 == 1:
	            return lst[n//2]
	    else:
	            return sum(lst[n//2-1:n//2+1])/2.0	

def getlisting(result,page_item_number,request):
	paginator = Paginator(result, page_item_number)
	page = request.GET.get('page')
	try:
		listing= paginator.page(page)
	except PageNotAnInteger:
		listing = paginator.page(1)
	except EmptyPage:
		listing = paginator.page(paginator.num_pages)

	return listing


def getContext(city,country,state,result,request,query,types,bedno,bathno,highlight):
	values=[int(property.value) for property in result]
	mid=median(values)
	count=result.count()
	true=Property.objects.filter(city__icontains=city)
	try:
		onebedroomcount=result.filter(Q(bedroom=1)).count()
		onebedroom=result.filter(bedroom=1).aggregate(Avg('value'))	
	except:
		onebedroomcount='0'
		onebedroom='0'
	request.session['onebedroomcount']=onebedroomcount
	try:
		twobedroomcount=result.filter(Q(bedroom=2)).count()
		twobedroom=result.filter(Q(bedroom=2)).aggregate(Avg('value'))
		#pdb.set_trace()	
	except:
		twobedroomcount='0'
		twobedroom='0'
	request.session['twobedroomcount']=twobedroomcount
	try:
		morebedroomcount=result.filter(Q(bedroom__gte=3)).count()
		morebedroom=result.filter(Q(bedroom__gte=3)).aggregate(Avg('value'))
	except:
		morebedroomcount='0'
		morebedroom='0'
	request.session['morebedroomcount']=morebedroomcount

	if true.exists():
		averages=Property.objects.values('state').annotate(Avg('value')).filter(Country__icontains=country)
		cityaverage=Property.objects.values('city').annotate(Avg('value')).filter(state__icontains=state)
		


	else:
		averages=Property.objects.values('state').annotate(Avg('value')).filter(Country__icontains=country)
		cityaverage=Property.objects.values('city').annotate(Avg('value')).filter(state__icontains=state)
		
	listing=getlisting(result,3,request)
	total=0
	counter=0
	for  property in result:
		total+=property.value
		counter+=1
	average_price= math.ceil(total/counter)
	values=[int(property.value) for property in result]
	midlist=median(values)
	try:
		pptysold=Sale.objects.values('state').annotate(Count('buyer')).get(pptystate__icontains=state)
		avgdeposit=Sale.objects.values('pptystate').annotate(Avg('down_payt')).get(pptystate__icontains=state)
		mediandeposit=Sale.objects.filter(pptystate__icontains=state)
		values=[int(property.down_payt) for property in mediandeposit]
		mediansale=median(values)


	except:
		pptysold='-'
		avgdeposit='-'
		mediansale='-'

	try:
		noofoffer=Offer.objects.values('state').annotate(Count('offerprice')).get(state__icontains=state)
	except :
		noofoffer='-'
	#pdb.set_trace()
	context={
	'result':listing,
	'count':count, 
	'state':query,
	'usestate':state,
	'city':city,
	'median':mid,
	'country':country,
	'averages':averages,
	'cityaverage':cityaverage,
	'topform':topForm(),
	'filterform':filterForm(),
	'onebedroom':onebedroom,
	'twobedroom':twobedroom,
	'morebedroom':morebedroom,
	'onebedroomcount':onebedroomcount,
	'twobedroomcount':twobedroomcount,
	'morebedroomcount':morebedroomcount,
	'averageprice':average_price,
	'medianprice':midlist,
	'avgdeposit':avgdeposit,
	'mediansale':mediansale,
	'noofoffer':noofoffer,
	'pptysold':pptysold,
	'hiddentype':types,
	'hiddenbedno':bedno,
	'hiddenbathno':bathno,
	'highlight':highlight,
	'today':date.today(),
	}		
	return context
def topFormFilter(types,bedno,bathno,result):
	if not types =='':
		result=result.filter(types__icontains=types)
					
	if not bedno == '' :
		if bedno =='more':
			result=result.filter(bedroom__gte='3')
			
		else:
			result=result.filter(bedroom__icontains=bedno)
			
	if not  bathno =='':
		if bathno =='more':
			result=result.filter(bathroom__gte='3')
			
		else:
			result=result.filter(bathroom__icontains=bathno)

	return result


def get_no_result_context(query='',request='',types='',bedno='',bathno='',result='', highlight='home'):
	result=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query))
	result=topFormFilter(types,bedno,bathno,result)
	try:
		city=result.latest('uploadDate').city
		state=result.latest('uploadDate').state
		country=result.latest('uploadDate').Country
		#pdb.set_trace()
		topFormFilter(types,bedno,bathno,result)
		listing=getlisting(result,3,request)
		averages=Property.objects.values('state').annotate(Avg('value')).filter(Country__icontains=country)
		cityaverage=Property.objects.values('city').annotate(Avg('value')).filter(state__icontains=state)
		count=result.count
		try:
			onebedroomcount=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query),bedroom=1).count()
			onebedroom=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query),bedroom=1).aggregate(Avg('value'))
		except:
			onebedroomcount='0'
		request.session['onebedroomcount']=onebedroomcount
		try:
			twobedroomcount=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query),bedroom=2).count()
			twobedroom=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query),bedroom=2).aggregate(Avg('value'))
		except:
			twobedroomcount='0'
		request.session['twobedroomcount']=twobedroomcount
		try:
			morebedroomcount=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query),bedroom__gte=3).count()
			morebedroom=onebedroom=Property.objects.filter(Q(state__icontains=query)|Q(city__icontains=query)|Q(Country__icontains=query)|Q(street__icontains=query),bedroom__gte=3).aggregate(Avg('value'))
		except:
			morebedroomcount='0'
		request.session['morebedroomcount']=morebedroomcount
		total=0
		counter=0
		for  property in result:
			total+=property.value
			counter+=1
		average_price= math.ceil(total/counter)
		values=[int(property.value) for property in result]
		midlist=median(values)
		try:
			pptysold=Sale.objects.values('state').annotate(Count('buyer')).get(pptystate__icontains=state)
			avgdeposit=Sale.objects.values('pptystate').annotate(Avg('down_payt')).get(pptystate__icontains=state)
			mediandeposit=Sale.objects.filter(pptystate__icontains=state)
			values=[int(property.down_payt) for property in mediandeposit]
			mediansale=median(values)


		except:
			pptysold='-'
			avgdeposit='-'
			mediansale='-'

		try:
			noofoffer=Offer.objects.values('state').annotate(Count('offerprice')).get(state__icontains=state)
		except :
			noofoffer='-'

		values=[int(property.value) for property in result]
		mid=median(values)
		context={
		'result':listing,
		'count':count, 
		'state':query,
		'usestate':state,
		'city':city,
		'median':mid,
		'country':country,
		'averages':averages,
		'cityaverage':cityaverage,
		'topform':topForm(),
		'filterform':filterForm(),
		'onebedroom':onebedroom,
		'twobedroom':twobedroom,
		'morebedroom':morebedroom,
		'onebedroomcount':onebedroomcount,
		'twobedroomcount':twobedroomcount,
		'morebedroomcount':morebedroomcount,
		'averageprice':average_price,
		'medianprice':midlist,
		'avgdeposit':avgdeposit,
		'mediansale':mediansale,
		'noofoffer':noofoffer,
		'pptysold':pptysold,
		'hiddentype':types,
		'hiddenbedno':bedno,
		'hiddenbathno':bathno,
		'highlight':highlight,
		}
		#pdb.set_trace()
		request.session['count']=result.count()
		request.session['query']=query
		return context

	except:
		if not result.exists():
			result=Property.objects.filter(feature=True)
			listing=getlisting(result,3,request)
			context={'result':listing,'topform':topForm(),'feature':True,'highlight':highlight}
			return context
	




	
	
	
	
	
