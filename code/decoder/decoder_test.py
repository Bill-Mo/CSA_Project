
from decoder import Decoder

# Test R type instruction

def R_test(): 
    # SUB x3 x3 x5
    imm = '0100000'
    rs2 = '00101'
    rs1 = '00011'
    rd = '00011'
    funct3 = '000'
    opcode = '0110011'
    ins = imm + rs2 + rs1 + funct3 + rd + opcode
    decoder = Decoder(ins)
    type, ins, rs2, rs1, rd = decoder.decode()
    assert(type == 'R')
    assert(ins == 'SUB')
    assert(rs2 == '00101')
    assert(rs1 == '00011')
    assert(rd == '00011')

    # XOR x30 x31 x0
    imm = '0000000'
    rs2 = '00000'
    rs1 = '11111'
    rd = '11110'
    funct3 = '100'
    opcode = '0110011'
    ins = imm + rs2 + rs1 + funct3 + rd + opcode
    decoder = Decoder(ins)
    type, ins, rs2, rs1, rd = decoder.decode()
    assert(type == 'R')
    assert(ins == 'XOR')
    assert(rs2 == '00000')
    assert(rs1 == '11111')
    assert(rd == '11110')

def I_test(): 
    # ANDI r10 r10 500
    imm = '000111110100'
    rs1 = '01010'
    rd = '01010'
    funct3 = '111'
    opcode = '0010011'
    ins = imm + rs1 + funct3 + rd + opcode
    decoder = Decoder(ins)
    type, ins, imm, rs1, rd = decoder.decode()
    assert(type == 'I')
    assert(ins == 'ANDI')
    assert(imm == '000111110100')
    assert(rs1 == '01010')
    assert(rd == '01010')

def S_test(): 
    # SW x8, 128(x7)
    imm11 = '0000100'
    rs2 = '01000'
    rs1 = '00111'
    imm4 = '00000'
    funct3 = '010'
    opcode = '0100011'
    ins = imm11 + rs2 + rs1 + funct3 + imm4 + opcode
    decoder = Decoder(ins)
    type, ins, imm, rs2, rs1 = decoder.decode()
    assert(type == 'S')
    assert(ins == 'SW')
    assert(imm == '000010000000')
    assert(rs2 == '01000')
    assert(rs1 == '00111')

def B_test(): 
    # BEQ x19, x10, 52
    imm12 = '0'
    imm11 = '000001'
    rs2 = '10011'
    rs1 = '01010'
    imm4 = '1010'
    imm1 = '0'
    funct3 = '000'
    opcode = '1100011'
    ins = imm12 + imm11 + rs2 + rs1 + funct3 + imm4 + imm1 + opcode
    decoder = Decoder(ins)
    type, ins, imm, rs2, rs1 = decoder.decode()
    assert(type == 'B')
    assert(ins == 'BEQ')
    assert(imm == '0000000110100')
    assert(rs2 == '10011')
    assert(rs1 == '01010')

def J_test():
    # JAL x16, 200
    imm = '00000000000011001000'
    rd = '10000'
    opcode = '1101111'
    ins = imm + rd + opcode
    decoder = Decoder(ins)
    type, ins, imm, rd = decoder.decode()
    assert(type == 'J')
    assert(ins == 'JAL')
    assert(imm == '00000000000011001000')
    assert(rd == '10000')
    assert(opcode == '1101111')

def Halt_test():
    # Halt
    imm = '0' * 25
    opcode = '1111111'
    ins = imm + opcode
    decoder = Decoder(ins)
    type, = decoder.decode()
    assert(type == 'H')

R_test()
I_test()
S_test()
B_test()
J_test()
Halt_test()
print('Test pass!')