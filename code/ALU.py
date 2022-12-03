def ALU_control(opcode, funct3, ALUop):
    if ALUop == 0b00: 
        return 0b0000
    elif ALUop == 0b01: 
        return 0b0110
    elif ALUop == 0b10: 
        if opcode == '0000000' and funct3 == '000': 
            return 0b0000
        elif opcode == '0100000' and funct3 == '000': 
            return 0b0110
        elif opcode == '0000000' and funct3 == '111': 
            return 0b0000
        elif opcode == '0000000' and funct3 == '110': 
            return 0b0001
        else: 
            return 0b0010


class ALU(object): 
    def __init__(self, ALU_control, input1, input2) -> None:
        output = 0

        if ALU_control == 0b0010: 
            output = self.do_add(input1, input2)
        elif ALU_control == 0b0110: 
            output = self.do_sub(input1, input2)
        elif ALU_control == 0b0000: 
            output = self.do_and(input1, input2)
        elif ALU_control == 0b0001: 
            output = self.do_or(input1, input2)

        return output
        
    def do_add(input1, input2): 
        return input1 + input2

    def do_sub(input1, input2): 
        return input1 - input2

    def do_and(input1, input2): 
        return input1 & input2

    def do_or(input1, input2): 
        return input1 | input2