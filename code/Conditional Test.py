# R-type operations
# Format: funct7(7 bits) rs2(5 bits) rs1(5 bits) funct3(3 bits) rd(5 bits) Opcode(7 bits) 
def Rtype(instr):
    funct3 = instruction[17:20] # funct3
    match funct3:
        case '000':
            if (instruction[:7] == "0000000"): # funct7
                ADD(instruction[7:12], instruction[12:17], instruction[20:25])
            elif (instruction[:7] == "0100000"): # funct7
                SUB(instruction[7:12], instruction[12:17], instruction[20:25])
            else:
                return "no such operation"
        case '100':
            XOR(instruction[7:12], instruction[12:17], instruction[20:25])
        case '110':
            OR(instruction[7:12], instruction[12:17], instruction[20:25])
        case '111':
            AND(instruction[7:12], instruction[12:17], instruction[20:25])
        case default:
            return "no such operation"

# I-type operations
# Format: imm[11:0] rs1(5 bits) funct3(3 bits) rd(5 bits) Opcode(7 bits)
def Itype(instr):
    funct3 = instruction[17:20] # funct3
    match funct3:
        case '000':
            ADDI(instruction[0:12], instruction[12:17], instruction[20:25])
        case '100':
            XORI(instruction[0:12], instruction[12:17], instruction[20:25])
        case '110':
            ORI(instruction[0:12], instruction[12:17], instruction[20:25])
        case '111':
            ANDI(instruction[0:12], instruction[12:17], instruction[20:25])
        case default:
            return "no such operation"

# B-type operations
# Format: imm[12, 10:5] rs2(5 bits) rs1(5 bits) funct3(3 bits) imm[4:1,11] Opcode(7 bits)
def Btype(instr):
    funct3 = instruction[17:20] # funct3
    match funct3:
        case '000':
            BEQ()
        case '001':
            BNE()
        case default:
            return "no such operation"

# Addition
def ADD(rs2, rs1, rd):
    rd = rs1 + rs2
    return

# Subtraction
def SUB(rs2, rs1, rd):
    rd = rs1 - rs2
    return

# Bitwise XOR
def XOR(rs2, rs1, rd):
    rd = rs1 ^ rs2
    return

# Bitwise OR
def OR(rs2, rs1, rd):
    rd = rs1|rs2
    return

# Bitwise AND
def AND(rs1, rs2, rd):
    rd = rs1&rs2
    return

# Add Immediate
def ADDI(imm, rs1, rd):
    return

# OR Immediate
def XORI(imm, rs1, rd):
    return

# OR Immediate
def ORI(imm, rs1, rd):
    return

# AND Immediate
def ANDI(imm, rs1, rd):
    return

# Jump and Link
def JAL(imm, rd):
    return

# Branch if equal
def BEQ(imm, rs2, rs1):
    return

# Branch if not equal
def BNE(imm, rs2, rs1):
    return

# Load Word
def LW():
    return

# Store Word
def SW():
    return

# Halt execution
def HALT():
    return


# According to Opcode to determine what type of the operation
def OpcodeDis(op, instr):
    match op:
        case '0110011':
            Rtype(instr)
        case '0010011':
            Itype(instr)
        case '1101111':
            imm = instruction[12] + instruction[20:29] + instruction[21] + instruction[13-20]
            JAL(imm, instruction[20:25])
        case '1100011':
            Btype(instr)
        case '0000011':
            LW()
        case '0100011':
            SW()
        case '1111111':
            HALT();    
        case default:
            return "no such operation"

# Assume the reading format is (funct7 rs2 rs1 funct3 rd opcode) 32-0
# 0000010 00001(instruction[7:12]) 00010(instruction[12:17]) 111 00100(instruction[20:25]) 0100100
instruction =  "00000100000100010111001000100100"
# get last 7 digit which is opcode
opcode = instruction[25:]
# print(opcode)
print(instruction[20:25])
# print(OpcodeDis(opcode, instruction))
# OpcodeDis(opcode, instruction)


