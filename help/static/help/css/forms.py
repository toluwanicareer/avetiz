from django import forms 

class SearchForm(forms.Form):
    help = forms.CharField(max_length=500)
    