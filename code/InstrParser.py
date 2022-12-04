def parse_instr(instr): 
    funct7 = instr[:6]
    rs2 = instr[7:12]
    rs1 = instr[12:17]
    funct3 = instr[17:20]
    rd = instr[20:25]
    opcode = instr[25:]
    sign_extended_imm = 

def ImmGen(instr): 
    