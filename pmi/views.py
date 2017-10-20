# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from home.forms import pmiForm
import pdb

# Create your views here.

class mortageList(ListView):
	template_name='pmi/product_list.html'
	model=Product

	def get_context_data(self, **kwargs):
		state=self.request.GET.get('pmi_state')
		country=self.request.GET.get('pmi_country')
		city=self.request.GET.get('pmi_city')
		query=self.request.GET.get('pmi_query')
		#pdb.set_trace()
		context=super(mortageList, self).get_context_data(**kwargs)
		if state:
			self.request.session['pmi_state']=state
			context['product_list']=Product.objects.filter(Q(min_price__lte=5000000),max_price__gte=5000000).filter(company__state__icontains=state)#remember it is here you will filter based on serach result
		else:
			context['product_list']=Product.objects.filter(Q(min_price__lte=5000000),max_price__gte=5000000).filter(Q(company__state__icontains=query)|Q(company__city__contains=query)|Q(company__country__icontains=query))
			self.request.session['pmi_state']=context['product_list'].latest('company__state').company.state
			#pdb.set_trace()
		context['now'] = timezone.now()
		context['count']=context['product_list'].count()
		context['mortage_value']=5000000
		context['percent']=20
		context['pmiform']=pmiForm()
		context['query']=query
		return context



def ajax_get_product_list(request):
	data=dict()
	principal=request.GET.get('principal')
	sort=request.GET.get('sort')
	if sort:
		if sort == 'fees':
			product_list=Product.objects.filter(Q(min_price__lte=principal),max_price__gte=principal).filter(company__state__icontains=request.session['pmi_state']).order_by('processing_fee')
		elif sort == 'rate':
			product_list=Product.objects.filter(Q(min_price__lte=principal),max_price__gte=principal).filter(company__state__icontains=request.session['pmi_state']).order_by('rate')
		elif sort == 'company':
			product_list=Product.objects.filter(Q(min_price__lte=principal),max_price__gte=principal).filter(company__state__icontains=request.session['pmi_state']).order_by('company__name')
	else :
		product_list=Product.objects.filter(Q(min_price__lte=principal),max_price__gte=principal).filter(company__state__icontains=request.session['pmi_state'])
	count=product_list.count()
	#pdb.set_trace()
	context={
	'product_list':product_list,
	}
	data['html_product_list']=render_to_string('pmi/includes/partial_product_list.html', context)
	data['count']=count
	data['principal']=principal
	return JsonResponse(data)












	