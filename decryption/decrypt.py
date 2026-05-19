from cryptography.fernet import Fernet

def decrypt_file(data,key):

    f = Fernet(key)

    decrypted = f.decrypt(data)

    return decrypted