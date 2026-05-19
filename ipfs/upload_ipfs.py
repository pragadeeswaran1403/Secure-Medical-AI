import requests

def upload_to_ipfs(file_path):

    url = "http://127.0.0.1:5001/api/v0/add"

    files = {"file": open(file_path,"rb")}

    response = requests.post(url, files=files)

    result = response.json()

    return result["Hash"]