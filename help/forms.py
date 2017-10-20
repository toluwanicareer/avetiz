from django import forms 
from .choices import PROFESSION_CHOICES

class SearchForm(forms.Form):
    help=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-lg', 'placeholder':'Search for Help'}))

class TopForm(forms.Form):
	help=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control tops', 'placeholder':'Search for Help'}))

class ComplaintForm(forms.Form):
	profession=forms.ChoiceField(label='Please tell us who you are',widget=forms.Select(attrs={'class':'form-control square'}),choices = PROFESSION_CHOICES)
	email=forms.EmailField(label='Your email address',widget=forms.EmailInput(attrs={'class':'form-control square'}))
	subject=forms.CharField(label='Subject',widget=forms.TextInput(attrs={'class':'form-control square'}))
	description=forms.CharField(label='Description',help_text='Please enter the details of your request. A member of our support staff will respond as soon as possible.',widget=forms.Textarea(attrs={'class':'form-control square','rows':'4'}))
	issue=forms.ChoiceField(label='Issue Type',widget=forms.Select(attrs={'class':'form-control square'}),choices = PROFESSION_CHOICES)
	#attachment=forms.FileField(label='Attachment',widget=forms.FileInput(attrs={'class':'form-control'}))

	

	
	
    