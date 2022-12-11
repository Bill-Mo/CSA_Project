from helper import *
import numpy as np
a = np.linspace(29, 40, 9)
b = np.linspace(32, 37, 9)

print(np.sum(a), np.sum(b))

'''
        0   1   2   3   4   5   6   7   8	9
0 LW    IF  ID  EX  MEM WB
4 LW        IF  ID  EX  MEM WB
8 ADD           IF  ID  ID  EX  MEM WB
12 SW               IF  IF  ID  EX  MEM WB
16 HALT                 ... IF  ID  EX  MEM	WB
'''

'''
        0   1   2	3	4	5	6	7	8	9	10
0 LW	IF	ID	EX	MEM	WB
4 ADDI		IF	ID	EX	MEM	WB
8 BNE			IF	ID	EX	MEM	WB
4 ADDI				...	IF	ID	EX	MEM	WB
8 BNE						IF	ID	EX	MEM	WB
12 HALT							IF	ID	EX	MEM	WB
'''