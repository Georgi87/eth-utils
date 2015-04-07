
EthJsonRpc:

```python
contract_code = open('contract.se').read()
rpc_client = EthJsonRpc('localhost, '8080')

contract_address = rpc_client.create_contract(contract_code=contract_code, value=1000000)['result']

rpc_client.eth_sendTransaction(contract_address, "function_name", [arg_1, arg_2], value=initial_funding, code=contract_code)

rpc_client.eth_call(contract_address, "function_name", [arg_1], code=contract_code)
```

Deploy Contracts:

```python

> deploy.py -f deploy_instructions.txt

instructions.txt:

create TAB contract_file_name

transact TAB contract_file_name TAB function_name TAB arg_1 TAB arg_2

Example:

create      contract1.se
create      contract2.se

transact    contract2.se     gain_access    contract1.se
# file names are replaced with contract addresses if contract was created by instruction before

```