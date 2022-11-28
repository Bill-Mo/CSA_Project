class ContorlUnit:
    def __init__(self):
        self.Branch = 0
        self.MemRead = 0
        self.MemtoReg = 0
        self.ALUOp = 0
        self.MemWrite = 0
        self.ALUSrc = 0
        self.RegWrite = 0

    def control(reset, opcode, Branch, MemRead, MemtoReg, ALUOp, MemWrite, ALUSrc, RegWrite):
        result = 0
        if opcode == 'R':
            ALUSrc = False
            MemtoReg = False
            RegWrite = True
            MemRead = False
            MemWrite = False
            Branch = False
            ALUOp = 2
            

        elif opcode == 'I':
            ALUSrc = True
            MemtoReg = True
            RegWrite = True
            MemRead = True
            MemWrite = False
            Branch = False
            ALUOp = 0

        elif opcode == 'S':
            ALUSrc = True
            MemtoReg = False
            RegWrite = False
            MemRead = False
            MemWrite = True
            Branch = False
            ALUOp = 0

        elif opcode == 'J':
            ALUSrc = False
            MemtoReg = False
            RegWrite = False
            MemRead = False
            MemWrite = False
            Branch = True
            ALUOp = 7