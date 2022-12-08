from helper import *
print('a' == 'b')

'''
        0   1   2   3   4   5   6   7   8
0 LW    IF  ID  EX  MEM WB
4 LW        IF  ID  EX  MEM WB
8 ADD           IF  ID  ID  EX  MEM WB
12 SW               IF  IF  ID  EX  MEM WB
16 HALT                 ... IF  ID  EX  MEM
'''