from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from .forms import selectAreaForm,castVoteForm,otpForm
from candidates.models import candidate
from elections.models import election
from web3 import Web3
from .models import vote as voteModel
from candidates.models import candidate
from django.contrib import messages
import requests
import json
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas as pd
# Create your views here.
API_KEY=getattr(settings,"API_KEY")
CONTRACT_ADDRESS=getattr(settings,"CONTRACT_ADDRESS")
ABI=getattr(settings,"ABI")

@login_required
def userHome(request):
	election=pd.read_csv(staticfiles_storage.path("Election.csv"))
	cols=list(election.columns)	
	rows=[]
	for i,j in election.iterrows():
		rows.append([j[0],j[1],j[2],j[3],j[4]])
	context={
		'cols':cols,
		'rows':rows
	}
	return render(request,"user_home.html",context)

def verifyVote(request):
	obj=voteModel.objects.filter(vname=request.user.fullname).all()
	context={
		'objects':obj
	}
	return render(request,'verify-vote.html',context)

def voteError(request):
	context={
		'message':'Vote already Cast'
	}
	return render(request,'vote-success.html',context)

def otpview(request):
	otpform=otpForm(request.POST or None,initial={'city':request.session['city'],'locality':request.session['local'],'candidate':request.session['cname']})
	context={
		'otpForm':otpform
	}
	if otpform.is_valid():
		current_user=request.user
		data=otpform.cleaned_data
		#print("Session ID 2:",request.session['session_id'])
		otp=str(data['otp'])
		#print(otp)
		#url="https://2factor.in/API/V1/"+API_KEY+"/SMS/VERIFY/"+request.session['session_id']+"/"+otp
		#response=requests.request("GET",url)
		#resp_json=json.loads(response.text)
		#print(resp_json)
		#status=resp_json['Status']
		status="Success"
		if(status=="Success"):
			_candidate=candidate.objects.get(cname=data['candidate'])
			w3=Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
			election_contract=w3.eth.contract(
				abi=ABI,
				address=CONTRACT_ADDRESS
			)
			account=w3.eth.accounts[current_user.id]
			tx_=election_contract.functions.vote(_candidate.id).transact({'from':account})
			reciept=w3.eth.waitForTransactionReceipt(tx_)
			# print(reciept)
			vote_obj=voteModel.objects.create(cname=_candidate.cname,vname=current_user.fullname,tx_hash=str(reciept['transactionHash']),block_hash=str(reciept['blockHash']))
			messages.success(request,"Your vote has been cast. Thank You.",extra_tags="alert-success")
			del request.session['city']
			del request.session['local']
			del request.session['cname']
			del request.session['session_id']
		else:
			messages.error(request,"Invalid OTP entered",extra_tags="alert-danger")
	return render(request,"otp.html",context)

def castVote(request):
	elections=election.objects.all().first()
	session_id=None
	if elections.get_status():
		areaForm=selectAreaForm(request.POST or None)
		voteForm=castVoteForm(None)
		context={
			'areaForm':areaForm
		}
		if areaForm.is_valid():
			data=areaForm.cleaned_data
			city=data['city']
			locality=data['locality']
			q=candidate.objects.search(locality)
			none_candidate=candidate.objects.get(cname="None")
			candidate_list=[(i,str(i)) for i in q]
			candidate_list.append((none_candidate,str(none_candidate)))
			voteForm=castVoteForm(request.POST or None,initial={'city':city,'locality':locality})
			voteForm.fields['candidate'].choices=candidate_list
			context['voteForm']=voteForm
			context['areaForm']=None
		if voteForm.is_valid():
			current_user=request.user
			data=voteForm.cleaned_data
			get_vote_obj = voteModel.objects.filter(vname=current_user.fullname)
			if get_vote_obj:
				messages.error(request,"You have already Voted",extra_tags="alert-danger")
			else:
				request.session['city']=data['city']
				request.session['local']=data['locality']
				request.session['cname']=data['candidate']	
				current_user=str(current_user)[3:0]
				#url="https://2factor.in/API/V1/"+API_KEY+"/SMS/"+current_user+"/AUTOGEN"
				#response= requests.request("GET",url)
				#resp_json=json.loads(response.text)
				#print(resp_json)
				#request.session['session_id']=resp_json['Details']
				request.session['session_id']="TEST"
				return redirect(reverse("otp"))
	else:
		context={
			'message':'Sorry the elections are currently closed.'
		}
	
	return render(request,"vote.html",context)