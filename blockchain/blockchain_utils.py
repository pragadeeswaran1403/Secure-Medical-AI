from web3 import Web3

# Connect Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

def is_connected():
    return web3.is_connected()

def store_hash(data_hash):
    try:
        accounts = web3.eth.accounts

        sender = accounts[0]
        receiver = accounts[1]

        tx = {
            'from': sender,
            'to': receiver,
            'value': 0,
            'gas': 21000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'nonce': web3.eth.get_transaction_count(sender)
        }

        tx_hash = web3.eth.send_transaction(tx)

        return web3.to_hex(tx_hash)

    except Exception as e:
        return f"Blockchain Error: {str(e)}"