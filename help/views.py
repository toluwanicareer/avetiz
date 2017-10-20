# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import Help
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import SearchForm
from .models import Help
from .forms import TopForm,ComplaintForm
from django.urls import reverse
from django.core.mail import EmailMessage

import json

def help_form(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)		
		if form.is_valid():
			tit= form.cleaned_data['help']
			try:
				form = TopForm()
				help=Help.objects.get(title=tit)
				return HttpResponseRedirect(reverse('help:detail', kwargs={'help_id':help.id}))
			except ObjectDoesNotExist:
				form = SearchForm()
				return render(request, 'help/helppage.html', {'form':form, 'error':'No results found for "'+tit+'"'})
		else:
			form = SearchForm()
			return render(request, 'help/helppage.html', {'form':form,'error':form.errors})
	else:
		form = SearchForm()
		return render(request, 'help/helppage.html', {'form':form})


def get_help(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		helps = Help.objects.filter(title__icontains = q )
		results = []
		for help in helps:
			help_json = {}
			help_json = help.title
			results.append(help_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def detailhelp(request, help_id='1'):
	if request.method=='POST':
		form=TopForm(request.POST)
		if form.is_valid():
			tit= form.cleaned_data['help']
			try:
				form=TopForm()
				help=Help.objects.get(title=tit)
				return render(request,'help/detailhelp.html', {'help':help, 'form':form})
			except ObjectDoesNotExist:
				return HttpResponseRedirect(reverse('help:detail', kwargs={'help_id':'1'}))
		else:
			form = TopForm()
			return render(request, 'help/detailhelp.html', {'form':form,'error':form.errors})
	else:
		form=TopForm()
		help=Help.objects.get(id=help_id)
		return render(request, 'help/detailhelp.html', {'form':form, 'help':help, 'message':'Please enter a keyword in the search box'})

def complaint(request):
	if request.method=='POST':
		form=ComplaintForm(request.POST)
		if form.is_valid():
			subject= form.cleaned_data['subject']
			email = EmailMessage(
								subject='Message From Avetiz Help Form. Subject: '+subject,
								body=form.cleaned_data['description'],
								from_email=form.cleaned_data['email'],
								to=['recruitment@avetiz.com'],
								reply_to=[form.cleaned_data['email']]
								)
			email.send(fail_silently=False)	
			return HttpResponseRedirect(reverse('help:helpform',current_app='help'))
		else:
			return render(request, 'help/complaintform.html', {'form':form, 'errors':form.errors})
	else:
		form=ComplaintForm()
		form2=TopForm()
		return render(request, 'help/complaintform.html', {'form':form, 'form2':form2})
	
		
	
			
