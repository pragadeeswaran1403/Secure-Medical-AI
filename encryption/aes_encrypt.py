from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)

def encrypt_image(data):

    cipher = AES.new(key,AES.MODE_EAX)

    ciphertext,tag = cipher.encrypt_and_digest(data)

    return cipher.nonce + tag + ciphertext