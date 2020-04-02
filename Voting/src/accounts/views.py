from django.shortcuts import render,redirect
from .forms import registerForm,loginForm
from django.contrib.auth import authenticate,login
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

def register_page(request):
	register_form=registerForm(request.POST or None,auto_id=False)
	context={
		"form":register_form
	}
	if register_form.is_valid():
		register_form.save()
		context={'messages':["Thank you. Click <a href='/login'>here</a> to login now."]}
	elif register_form.errors:
		context['errors']=register_form.errors
	return render(request,"register.html",context)

def login_page(request):
	login_form=loginForm(request.POST or None)
	context={
		"form":login_form
	}
	if login_form.is_valid():
		data=login_form.cleaned_data
		phonenumber=data.get("phonenumber")
		password=data.get("password")
		user=authenticate(request,username=phonenumber,password=password)
		if user is None:
			#raise ValidationError("Phone Number and Password do not match. Please try again")
			messages.error(request,"Phone Number and Password do not match. Try again.",extra_tags="alert-danger")
		else:
			login(request,user)
			return redirect("userHome")
	elif login_form.errors:
		context['errors']=login_form.errors
	return render(request,"login.html",context)

def account_home_view(request):
	return render(request,'account-home.html',{})