from web3 import Web3
from solcx import set_solc_version,compile_files,link_code

set_solc_version('v0.5.16')

def deploy_contract(contract_interface):
    # Instantiate and deploy contract
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    # Get transaction hash from deployed contract
    tx_hash = contract.deploy(
        transaction={'from': w3.eth.accounts[1]}
    )
    # Get tx receipt to get contract address
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    return tx_receipt['contractAddress']

w3=Web3(Web3.HTTPProvider("https://127.0.0.1:8545"))
contracts=compile_files(['./contracts/Election.sol'])

main_contract = contracts.pop("./contracts/Election.sol:Election")
print(main_contract['abi'])


'''
Replacing 'Election'
   --------------------
   > transaction hash:    0x1306bcb7351215c43889bd92ec53c57fee2b6c4abf96a7f72a66fd788c4198ba
   > Blocks: 0            Seconds: 0
   > contract address:    0x6CaC6014c8a96481Fc0c8F5cb627538e8A194Ff7
   > block number:        7
   > block timestamp:     1583479453
   > account:             0xE50376b13f124B3D0733dE99eD51582dd5DAdFA9
   > balance:             99.97576514
   > gas used:            385685
   > gas price:           20 gwei
   > value sent:          0 ETH
   > total cost:          0.0077137 ETH


   > Saving migration to chain.
   > Saving artifacts
   -------------------------------------
   > Total cost:           0.0077137 ETH

main_contract['bin'] = link_code(main_contract['bin'])

contract_address = deploy_contract(main_contract)

with open('data.json', 'w') as outfile:
    data = {
       "abi": main_contract['abi'],
       "contract_address": deploy_contract(main_contract)
    }
    json.dump(data, outfile, indent=4, sort_keys=True)

'''