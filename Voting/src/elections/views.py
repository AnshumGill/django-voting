from django.shortcuts import render
from web3 import Web3
from candidates.models import candidate
from django.conf import settings
# Create your views here.
ABI=getattr(settings,"ABI")
CONTRACT_ADDRESS=getattr(settings,"CONTRACT_ADDRESS")

def result(request):
    candidates_list = candidate.objects.all()
    context={
        'res':[]
    }
    w3=Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    election_contract=w3.eth.contract(
        abi=ABI,
        address=CONTRACT_ADDRESS,
    )
    admin_acc = w3.eth.accounts[0]
    for c in candidates_list:
        getVote=election_contract.functions.getVote(c.id).call()
        if(str(c) != "None"):
            context['res'].append({'cname':c.cname,'votes':getVote,'affiliation':c.affiliation.pname,'location':c.location})
        else:
            context['res'].append({'cname':c.cname,'votes':getVote,'affiliation':"-",'location':"-"})
    return render(request,"results.html",context)

