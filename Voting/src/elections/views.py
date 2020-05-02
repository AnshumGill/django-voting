from django.shortcuts import render
from web3 import Web3
from candidates.models import candidate
# Create your views here.
ABI=[{'inputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'uint256', 'name': '_candidateId', 'type': 'uint256'}], 'name': 'votedEvent', 'type': 'event'}, {'constant': True, 'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'candidates', 'outputs': [{'internalType': 'uint256', 'name': 'id', 'type': 'uint256'}, {'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'uint256', 'name': 'voteCount', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'candidatesCount', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'uint256', 'name': '_candidateId', 'type': 'uint256'}], 'name': 'getVote', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'uint256', 'name': '_candidateId', 'type': 'uint256'}], 'name': 'vote', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'name': 'voters', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}]
CONTACT_ADDRESS="0x3329F52AA646bBb07dE85a86Db272E00F51D3cdA"


def result(request):
    candidates_list = candidate.objects.all()
    context={
        'res':[]
    }
    w3=Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    election_contract=w3.eth.contract(
        abi=ABI,
        address=CONTACT_ADDRESS,
    )
    admin_acc = w3.eth.accounts[0]
    for c in candidates_list:
        getVote=election_contract.functions.getVote(c.id).call()
        context['res'].append({'cname':c.cname,'votes':getVote,'affiliation':c.affiliation.pname,'location':c.location})
    return render(request,"results.html",context)

