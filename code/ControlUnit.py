class ContorlUnit:
    def __init__(self):
        self.Branch = 0
        self.MemRead = 0
        self.MemtoReg = 0
        self.ALUOp = 0
        self.MemWrite = 0
        self.ALUSrc = 0
        self.RegWrite = 0

    def control(self, opcode):
        if opcode == 'R':
            self.ALUSrc = False
            self.MemtoReg = False
            self.RegWrite = True
            self.MemRead = False
            self.MemWrite = False
            self.Branch = False
            self.ALUOp = 2
            

        elif opcode == 'I':
            self.ALUSrc = True
            self.MemtoReg = True
            self.RegWrite = True
            self.MemRead = True
            self.MemWrite = False
            self.Branch = False
            self.ALUOp = 0

        elif opcode == 'S':
            self.ALUSrc = True
            self.MemtoReg = False
            self.RegWrite = False
            self.MemRead = False
            self.MemWrite = True
            self.Branch = False
            self.ALUOp = 0

        elif opcode == 'J':
            self.ALUSrc = False
            self.MemtoReg = False
            self.RegWrite = False
            self.MemRead = False
            self.MemWrite = False
            self.Branch = True
            self.ALUOp = 7