class Decoder(object):
    def __init__(self, instr) -> None:
        assert(len(instr) == 32)

        self.instr = instr
        self.funct7 = self.instr[:7]
        self.funct3 = self.instr[17:20]
        self.opcode = self.instr[25:]

    def decode(self): 
        
        type = self.type_decode()
        rs1 = self.instr[12:17]
        rs2 = self.instr[7:12]
        rd = self.instr[20:25]

        if type == 'R': 
            ins = self.R_instr_decode()
            return (type, ins, rs2, rs1, rd)
        
        elif type == 'I': 
            imm = self.instr[:12]
            ins = self.I_instr_decode()
            return (type, ins, imm, rs1, rd)
        
        elif type == 'S': 
            imm = self.instr[:7] + self.instr[20:25]
            ins = self.S_instr_decode()
            return (type, ins, imm, rs2, rs1)

        elif type == 'B': 
            imm = self.instr[0] + self.instr[-8] + self.instr[1:7] + self.instr[20:24] + '0'
            ins = self.B_instr_decode()
            return (type, ins, imm, rs2, rs1)

        elif type == 'J':
            imm =  self.instr[:20]
            ins = self.J_instr_decode()
            return (type, ins, imm, rd)
        
        else: 
            return (type, )

    def type_decode(self): 
        opcode = self.opcode

        if opcode == '0110011': 
            return 'R'
        elif opcode == '0010011' or opcode == '0000011': 
            return 'I'
        elif opcode == '1101111': 
            return 'J'
        elif opcode == '1100011': 
            return 'B'
        elif opcode == '0100011': 
            return 'S'
        elif opcode == '1111111': 
            return 'H'
        else: 
            print(opcode)
            raise Exception('Wrong instruction type')

    def R_instr_decode(self): 
        funct3 = self.funct3
        funct7 = self.funct7

        if funct3 == '000': 
            if funct7 == '0000000': 
                return 'ADD'
            elif funct7 == '0100000': 
                return 'SUB'
            else: 
                raise Exception('Wrong instruction. In R type instruction decoder')
        elif funct3 == '100':
            return 'XOR' 
        elif funct3 == '110': 
            return 'OR'
        elif funct3 == '111': 
            return 'AND'
        else: 
            raise Exception('Wrong instruction. In R type instruction decoder')

    def B_instr_decode(self): 
        funct3 = self.funct3

        if funct3 == '000': 
            return 'BEQ'
        elif funct3 == '001': 
            return 'BNE'
        else: 
            raise Exception('Wrong instruction. In B type instruction decoder')

    def S_instr_decode(self): 
        return 'SW'

    def J_instr_decode(self): 
        return 'JAL'


    def I_instr_decode(self): 
        funct3 = self.funct3
        opcode = self.opcode

        if funct3 == '000': 
            if opcode == '0010011': 
                return 'ADDI'
            elif opcode == '0000011': 
                return 'LW'
            else: 
                raise Exception('Wrong instruction. In I type instruction decoder')
        elif funct3 == '100': 
            return 'XORI'
        elif funct3 == '110': 
            return 'ORI'
        elif funct3 == '111': 
            return 'ANDI'
        else: 
            raise Exception('Wrong instruction. In I type instruction decoder')