class Conditional(object):
    def __init__(self, type, ins, rs2, rs1, rd) -> None:
        return control(type, ins, rs2, rs1, rd)

    # Addition
    def ADD(rs2, rs1):
        return rs1 + rs2

    # Subtraction
    def SUB(rs2, rs1):
        return rs1 - rs2
        
    # Bitwise XOR
    def XOR(rs2, rs1):
        return rs1 ^ rs2

    # Bitwise OR
    def OR(rs2, rs1):
        return rs1 | rs2

    # Bitwise AND
    def AND(rs1, rs2):
        return rs1 & rs2

    # Add Immediate
    def ADDI(imm, rs1):
        return rs1 + imm

    # OR Immediate
    def XORI(imm, rs1):
        return rs1 ^ imm

    # OR Immediate
    def ORI(imm, rs1):
        return rs1 | imm

    # AND Immediate
    def ANDI(imm, rs1):
        return rs1 & imm

    # Jump and Link
    def JAL(imm, rd):
        return

    # Branch if equal
    def BEQ(rs2, rs1):
        return rs2 == rs1

    # Branch if not equal
    def BNE(rs2, rs1):
        return rs2 != rs1

    # Load Word
    def LW():
        return

    # Store Word
    def SW():
        return

    # Halt execution
    def HALT():
        return

    # R-type operations
    # Format: funct7(7 bits) rs2(5 bits) rs1(5 bits) funct3(3 bits) rd(5 bits) Opcode(7 bits) 
    def Rtype(type, ins, rs2, rs1, rd):
        funct3 = ins[17:20] # funct3
        if funct3 == '000':
            if (ins[:7] == "0000000"): # funct7
                ADD(rs2, rs1, rd)
            elif (ins[:7] == "0100000"): # funct7
                SUB(rs2, rs1, rd)
            else:
                return "no such operation"
        elif funct3 =='100':
            XOR(rs2, rs1, rd)
        elif funct3 =='110':
            OR(rs2, rs1, rd)
        elif funct3 =='111':
            AND(rs2, rs1, rd)
        else:
            return "no such operation"

    # I-type operations
    # Format: imm[11:0] rs1(5 bits) funct3(3 bits) rd(5 bits) Opcode(7 bits)
    def Itype(type, ins, imm, rs1, rd):
        funct3 = ins[17:20] # funct3
        if funct3 =='000':
            ADDI(ins[0:12], rs1, rd)
        elif funct3 == '100':
            XORI(ins[0:12], rs1, rd)
        elif funct3 == '110':
            ORI(ins[0:12], rs1, rd)
        elif funct3 == '111':
            ANDI(ins[0:12], rs1, rd)
        else:
            return "no such operation"

    # S-type operations
    def S_Type (type, ins, imm, rs1, rd):
        SW()

    # B-type operations
    # Format: imm[12, 10:5] rs2(5 bits) rs1(5 bits) funct3(3 bits) imm[4:1,11] Opcode(7 bits)
    def Btype(type, ins, imm, rs1, rd):
        funct3 = ins[17:20] # funct3
        if funct3 == '000':
            BEQ()
        elif funct3 == '001':
            BNE()
        else:
            return "no such operation"

    def control(self, instr, type, ins, rs2, rs1, rd):
        if instr == 'R':
            Rtype(type, ins, rs2, rs1, rd)
        elif type == 'I':
            Itype(type, ins, rs2, rs1, rd)
        elif type == 'S':
            Stype(type, ins, rs2, rs1, rd)
        elif type == 'B':
            Btype(type, ins, rs2, rs1, rd)
        else:
            return "no such operation"
            




    # # According to Opcode to determine what type of the operation
    # def OpcodeDis(op, instr):
    #     match op:
    #         case '0110011':
    #             Rtype(instr)
    #         case '0010011':
    #             Itype(instr)
    #         case '1101111':
    #             imm = ins[12] + ins[20:29] + ins[21] + ins[13-20]
    #             JAL(imm, rd)
    #         case '1100011':
    #             Btype(instr)
    #         case '0000011':
    #             LW()
    #         case '0100011':
    #             SW()
    #         case '1111111':
    #             HALT();    
    #         case default:
    #             return "no such operation"

    # Assume the reading format is (funct7 rs2 rs1 funct3 rd opcode) 32-0
    # 0000010 00001(rs2) 00010(rs1) 111 00100(rd) 0100100
    # ins =  "00000100000100010111001000100100"
    # # get last 7 digit which is opcode
    # opcode = ins[25:]
    # # print(opcode)
    # print(rd)
    # print(OpcodeDis(opcode, ins))
    # OpcodeDis(opcode, ins)


