from encryption.aes_encrypt import encrypt_image
from encryption.dna_encrypt import dna_encode

def hybrid_encrypt(data):

    aes = encrypt_image(data)

    dna = dna_encode(aes)

    return dna
