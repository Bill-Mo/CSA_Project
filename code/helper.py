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
    if bit < 0 : 
        reverse_bit = -bit - 1
        reverse_bitstr = bin(reverse_bit)[2:]
        bitstr = ''
        for bit in reverse_bitstr: 
            if bit == '1':
                bitstr += '0'
            else: 
                bitstr += '1'

        if len(bitstr) > 32:
            bitstr = bitstr[-32:]
        while len(bitstr) < 32: 
            bitstr = '1' + bitstr
    else: 
        bitstr = bin(bit)[2:]
        if len(bitstr) > 32:
            bitstr = bitstr[-32:]
        
        while len(bitstr) < 32: 
            bitstr = '0' + bitstr
    return bitstr


def bitstr_to_int(bitstr):
    if isinstance(bitstr, int): 
        return bitstr
    integer = int(bitstr, 2)
    bitlen = len(bitstr)
    if (integer & (1 << (bitlen - 1))) != 0:
        integer = integer - (1 << bitlen)
    return integer