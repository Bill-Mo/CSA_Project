def swap(x5, x6): 
    x6 = x5 ^ x6
    x5 = x5 ^ x6
    x6 = x5 ^ x6
    return (x5, x6)
print(swap(145, 2222))