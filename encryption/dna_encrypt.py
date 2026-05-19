def dna_encode(data):

    mapping = {
        '00':'A',
        '01':'T',
        '10':'C',
        '11':'G'
    }

    binary = ''.join(format(byte,'08b') for byte in data)

    dna=""

    for i in range(0,len(binary),2):
        pair=binary[i:i+2]
        dna+=mapping.get(pair,'A')

    return dna