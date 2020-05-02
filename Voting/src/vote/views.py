from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import selectAreaForm,castVoteForm
from candidates.models import candidate
from elections.models import election
from web3 import Web3
from .models import vote as voteModel
from candidates.models import candidate
# Create your views here.

ABI=[{'inputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'uint256', 'name': '_candidateId', 'type': 'uint256'}], 'name': 'votedEvent', 'type': 'event'}, {'constant': True, 'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'candidates', 'outputs': [{'internalType': 'uint256', 'name': 'id', 'type': 'uint256'}, {'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'uint256', 'name': 'voteCount', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'candidatesCount', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'uint256', 'name': '_candidateId', 'type': 'uint256'}], 'name': 'getVote', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'uint256', 'name': '_candidateId', 'type': 'uint256'}], 'name': 'vote', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'name': 'voters', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}]
CONTACT_ADDRESS="0x3329F52AA646bBb07dE85a86Db272E00F51D3cdA"

@login_required
def userHome(request):
	return render(request,"user_home.html",{})

def verifyVote(request):
	obj=voteModel.objects.filter(vname=request.user.fullname).all()
	'''
	w3=Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
	election_contract=w3.eth.contract(
		abi=ABI,
		address=CONTACT_ADDRESS
	)
	getvote=election_contract.functions.getVote(1).call()
	print(getvote)
	'''
	context={
		'objects':obj
	}
	return render(request,'verify-vote.html',context)

def voteError(request):
	context={
		'message':'Vote already Cast'
	}
	return render(request,'vote-success.html',context)

def castVote(request):
	elections=election.objects.all().first()
	if elections.get_status():
		areaForm=selectAreaForm(request.POST or None)
		voteForm=castVoteForm(None)
		context={
			'areaForm':areaForm,
		}
		if areaForm.is_valid():
			data=areaForm.cleaned_data
			city=data['city']
			locality=data['locality']
			q=candidate.objects.search(locality)
			candidate_list=[(i,str(i)) for i in q]
			voteForm=castVoteForm(request.POST or None,initial={'city':city,'locality':locality})
			voteForm.fields['candidate'].choices=candidate_list
			context['voteForm']=voteForm
		if voteForm.is_valid():
			# VOTE HERE, BLOCKCHAIN STUFF
			current_user=request.user
			data=voteForm.cleaned_data
			_candidate=candidate.objects.get(cname=data['candidate'])
			w3=Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
			get_vote_obj = voteModel.objects.filter(vname=current_user.fullname)
			if get_vote_obj:
				context['error']=True
			else:
				context['error']=False
				election_contract=w3.eth.contract(
					abi=ABI,
					address=CONTACT_ADDRESS
				)
				account=w3.eth.accounts[current_user.id - 1]
				tx_=election_contract.functions.vote(_candidate.id).transact({'from':account})
				reciept=w3.eth.waitForTransactionReceipt(tx_)
				vote_obj=voteModel.objects.create(cname=_candidate.cname,vname=current_user.fullname,tx_hash=str(reciept['transactionHash']),block_hash=str(reciept['blockHash']))
	else:
		context={
			'message':'Sorry the elections are currently closed.'
		}
	
	return render(request,"vote.html",context)