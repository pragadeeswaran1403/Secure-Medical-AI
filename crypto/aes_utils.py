from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

def get_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_aes(data, password):
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ct

def decrypt_aes(enc_data, password):
    key = get_key(password)
    iv = enc_data[:16]
    ct = enc_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size)