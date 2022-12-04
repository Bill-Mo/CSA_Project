class BitToInt(object):
    def __init__(self, val, bit) -> None:
        return self.twos_comp(val, bit)

    # val is string type of bits
    # bits is the sign bit
    def twos_comp(val, bits):
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)
        return val

    # Example
    binary_string = '00001010'
    out = twos_comp(int(binary_string,2), len(binary_string))

    print(out)