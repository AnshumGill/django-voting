from django.shortcuts import render
from .forms import partyInfoForm
from .models import party
# Create your views here.

def partyInfo(request):
	partyForm=partyInfoForm(request.POST or None)
	context={
		'form':partyForm,
		'formSubmitted':False,
	}
	if partyForm.is_valid():
		context['formSubmitted']=True
		data=partyForm.cleaned_data
		pname=data['partyname']
		q=party.objects.filter(pname=pname).first()
		context['members']=q.members.all()
		
	return render(request,'party-info.html',context)