from django import forms

class queryForm(forms.Form):
	query=forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control input-lg', 'placeholder':'Enter an Address, City, Suburb, Neighborhood or Zip Code '}))
	city=forms.CharField(label="",widget=forms.HiddenInput(),required=False)
	state=forms.CharField(label="",widget=forms.HiddenInput(),required=False)
	country=forms.CharField(label="",widget=forms.HiddenInput(),required=False)

class pmiForm(forms.Form):
	pmi_query=forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control input-lg', 'placeholder':'Enter an Address, City, State, Neighborhood or Zip Code '}))
	pmi_city=forms.CharField(label="",widget=forms.HiddenInput(),required=False)
	pmi_state=forms.CharField(label="",widget=forms.HiddenInput(),required=False)
	pmi_country=forms.CharField(label="",widget=forms.HiddenInput(),required=False)
