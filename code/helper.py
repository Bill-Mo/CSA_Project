# Convert a binary bit to srting and pad zeros in the front
def int_to_bitstr(bit: int) ->str: 
    '''

    Convert a int to a 32 bits binary srting and pad zeros in the front.

    '''
    if not isinstance(bit, int):
        if isinstance(bit, str): 
            while len(bit) < 32: 
                bit = '0' + bit 
            return bit
        else: 
            raise Exception('The input is neither a int nor a string')
    
    bit = bin(bit)[2:]
    if len(bit) > 32:
        raise Exception('Too big data with length {}'.format(len(bit)))
    
    while len(bit) < 32: 
        bit = '0' + bit
    return bit


def bitstr_to_int(bitstr): 
    if len(bitstr) == 32 and bitstr[0] == '1': 
        for i, bit in enumerate(bitstr): 
            if bit == '0': 
                bitstr[i] = '1'
            else: 
                bitstr[i] = '0'
    return bitstr