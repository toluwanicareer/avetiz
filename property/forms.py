from django import forms 
from choices import COLUMN_CHOICES,LIMIT_CHOICES, PRICE_CHOICES

class SortForm(forms.Form):
	order_by_column=forms.ChoiceField(label='Issue Type',widget=forms.Select(attrs={'class':'form-control','onchange':'ajaxSubmit()','value':'{{orderby}}'}),choices = COLUMN_CHOICES)
	limit=forms.ChoiceField(label='Sort by', widget=forms.Select(attrs={'class':'form-control','onchange':'ajaxSubmit()', 'value':'{{limitby}}'}),choices=LIMIT_CHOICES)
class filterForm(forms.Form):
	minprice=forms.ChoiceField(label="",widget=forms.Select(attrs={'class':'form-control'}),choices=PRICE_CHOICES, required=False)
	maxprice=forms.ChoiceField(label="",widget=forms.Select(attrs={'class':'form-control'}) ,choices=PRICE_CHOICES, required=False)
	filtercity=forms.CharField(label="",widget=forms.HiddenInput(), required=False)
	filterstate=forms.CharField(label="",widget=forms.HiddenInput(), required=False)
	filtercountry=forms.CharField(label="",widget=forms.HiddenInput(), required=False)
class searchForm(forms.Form):
	query=forms.CharField()

class topForm(forms.Form):
	search=forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Address, City, Neighborhood" ,'autocomplete':'off' ,'autofocus':'autofocus' }))
	city=forms.CharField(label="",widget=forms.HiddenInput(), required=False)
	state=forms.CharField(label="",widget=forms.HiddenInput(), required=False)
	country=forms.CharField(label="",widget=forms.HiddenInput(), required=False)
   	#minprice=forms.CharField(label="",widget=forms.NumberInput(attrs={ 'class':"form-control" ,'placeholder':"No Max" ,'data-role':"facet-input-max", 'maxlength':"11" ,'size':"11" ,'id':"facet-input-max" }),required=False)
   	#maxprice=forms.CharField(label="",widget=forms.NumberInput(attrs={ 'class':"form-control" ,'placeholder':"No Max" ,'data-role':"facet-input-max", 'maxlength':"11" ,'size':"11" ,'id':"facet-input-max"}),required=False)
	propertytype=forms.CharField(label="", widget=forms.HiddenInput(), required=False)
	bedno=forms.CharField(label="", widget=forms.HiddenInput(), required=False)
	bathno=forms.CharField(label="", widget=forms.HiddenInput(), required=False)
class detailcontactform(forms.Form):
	firstname=forms.CharField(label="First Name", widget=forms.TextInput(attrs={'placeholder':'Firstname','class':'form-control'}))
	lastname=forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'placeholder':'Lastname','class':'form-control'}))
	email=forms.EmailField(label="Email address",widget=forms.TextInput(attrs={'placeholder':'Email','class':'form-control'}))
	phone=forms.CharField(label='Phone', widget=forms.TextInput(attrs={'placeholder':'Phone','class':'form-control'}))
	buy=forms.BooleanField(label="Buying", widget=forms.CheckboxInput(attrs={}))
	sell=forms.BooleanField(label="Selling", widget=forms.CheckboxInput(attrs={}))
	message=forms.CharField(label="What can we for you?", widget=forms.Textarea(attrs={'class':'form-control','row':'4'}))

class shareform(forms.Form):
	notes=forms.CharField(label="Notes", widget=forms.TextInput(attrs={'class':'form-control'}))
	email=forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control'}))

class detailContactFormTop(forms.Form):
	name=forms.CharField(label="First Name", widget=forms.TextInput(attrs={'placeholder':'Firstname','class':'form-control'}))
	email=forms.EmailField(label="Email address",widget=forms.TextInput(attrs={'placeholder':'Email','class':'form-control'}))
	phone=forms.CharField(label='Phone', widget=forms.TextInput(attrs={'placeholder':'Phone','class':'form-control'}))
	subject=forms.CharField(label='Subject', widget=forms.TextInput(attrs={'placeholder':'Subject', 'class':'form-control'}))
	message=forms.CharField(label='Message', widget=forms.Textarea(attrs={'placeholder':'Message', 'class':'form-control'}))


