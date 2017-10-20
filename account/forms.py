from django import forms 

class LoginForm(forms.Form):
	email=forms.EmailField(label='Email Address:',widget=forms.EmailInput(attrs={'class':'form-control '}))
	password=forms.CharField(label='Password:',widget=forms.PasswordInput(attrs={'class':'form-control'}))