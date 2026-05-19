from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

def store_hash(hash_value):

    if web3.is_connected():

        account = web3.eth.accounts[0]

        tx = {
            'from': account,
            'to': account,
            'value': 0,
            'gas': 2000000,
            'gasPrice': web3.to_wei('20','gwei'),
            'nonce': web3.eth.get_transaction_count(account),
            'data': hash_value.encode()
        }

        tx_hash = web3.eth.send_transaction(tx)

        return tx_hash.hex()

    else:
        return None