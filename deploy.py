from jsonrpc import EthJsonRpc
import click
import time

@click.command()
@click.option('-f', help='File with instructions.')
@click.option('-host', default="localhost", help='Ethereum server host.')
@click.option('-port', default='8080', help='Ethereum server port.')
def setup(f, host, port):

    def wait_for_new_block(last_block_no):
        while last_block_no == json_rpc.eth_blockNumber():
            time.sleep(1)
        return json_rpc.eth_blockNumber()

    instructions = [line.strip().split('\t') for line in open(f) if line]
    json_rpc = EthJsonRpc(host, port)
    block_no = 0
    addresses = {}
    for instruction in instructions:
        if instruction[0].startswith('#'):
            continue
        elif instruction[0] == 'create':
            file_name = instruction[1]
            code = open(file_name).read()
            print 'Try to create contract based on code in file: {}'.format(file_name)
            block_no = wait_for_new_block(block_no)
            contract_address = json_rpc.create_contract(code)['result']
            print 'Create contract transaction sent. Contract {} was created at address {}.'.format(file_name, contract_address)
            addresses[file_name] = contract_address
        elif instruction[0] == 'transact':
            to = instruction[1]
            if to in addresses:
                # function call
                function_name = instruction[2]
                data = [int(addresses[argument], 16) if argument in addresses else argument for argument in instruction[3:]]
                print 'Call transaction to function {} in contract {} with arguments {}.'.format(function_name, to, data)
                block_no = wait_for_new_block(block_no)
                code = open(to).read()
                json_rpc.eth_sendTransaction(addresses[to], function_name, data, code=code)
            else:
                # simple transaction
                pass
        elif instruction[0] == 'call':
            # call function
            pass
        elif instruction[0] == 'assert':
            # assert function
            pass


if __name__ == '__main__':
    setup()