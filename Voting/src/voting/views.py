from django.shortcuts import render,redirect
#from vote.views import userHome

def index(request):
	if request.user.is_authenticated:
		return redirect("userHome")
	else:
		return render(request,"index.html",{})
