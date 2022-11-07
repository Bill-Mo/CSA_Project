# Convert a binary bit to srting and pad zeros in the front
def int_to_32str(bit: int) ->str: 
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
            raise Exception('Too big data')

    while len(bit) < 32: 
            bit = '0' + bit
    
    return bit