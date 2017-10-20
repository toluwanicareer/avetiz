# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as authlogin, logout as authlogout
from django.shortcuts import render
from .forms import LoginForm
def login(request):
	form=LoginForm()
	return render(request,'account/login.html',{'form':form})


