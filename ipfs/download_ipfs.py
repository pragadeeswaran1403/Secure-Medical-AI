import requests

def download_from_ipfs(hash):

    url = "https://ipfs.io/ipfs/" + hash

    r = requests.get(url)

    with open("downloaded.txt","wb") as f:
        f.write(r.content)

    return "downloaded.txt"