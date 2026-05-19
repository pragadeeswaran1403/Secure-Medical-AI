import ipfshttpclient

def upload_to_ipfs(file_path):
    try:
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        res = client.add(file_path)
        return res['Hash']
    except Exception as e:
        return f"IPFS Error: {str(e)}"