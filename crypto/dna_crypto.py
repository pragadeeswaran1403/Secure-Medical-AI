def dna_encode(data):
    binary = ''.join(format(byte, '08b') for byte in data)

    dna_map = {
        "00": "A",
        "01": "T",
        "10": "C",
        "11": "G"
    }

    dna = ''.join(dna_map[binary[i:i+2]] for i in range(0, len(binary), 2))
    return dna