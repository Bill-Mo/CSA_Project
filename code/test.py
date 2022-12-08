from helper import *
def step(self):
        # Your implementation

        # 1. Fetch instruction from memory.
        PC = self.state.IF['PC']
        instr = self.ext_imem.readInstr(PC)

        # 2. Read registers and decode the instruction.
        parser = Parser(instr)
        funct7 = parser.funct7
        funct3 = parser.funct3
        opcode = parser.opcode
        type, ins, rs2_raw, rs1_raw, rd_raw = parser.parse()
        imm_raw = ImmGen(instr, type)
        rs2 = int(rs2_raw, 2)
        rs1 = int(rs1_raw, 2)
        rd = int(rd_raw, 2)
        imm = bitstr_to_int(imm_raw)
        print('{}\t{}\tx{}\tx{}\tx{}\t{}'.format(self.cycle, ins, rd, rs1, rs2, imm))

        
        if type == 'H': 
            self.state.IF['nop'] = True
            self.state.ID['nop'] = True
            self.state.EX['nop'] = True
            self.state.MEM['nop'] = True
            self.state.WB['nop'] = True
            
        self.state.ID['Instr'] = instr

        # 3. Execute the operation or calculate an address.
        rs1_data_raw = self.myRF.readRF(rs1)
        rs2_data_raw = self.myRF.readRF(rs2)
        if type == 'J': 
            rs1_data_raw = int_to_bitstr(PC)
            rs2_data_raw = int_to_bitstr(4)

        main_con = ControlUnit(type, ins)
        ALU_con = ALU_control(opcode, funct7, funct3, main_con.ALUOp)
        input2_raw = self.EX_MUX(rs2_data_raw, imm_raw, main_con.ALUSrc)

        ALU_output = ALU(ALU_con, ins, rs1_data_raw, input2_raw)

        # Branch
        if type != 'H':
            if ins == 'BEQ': 
                ALU_output = ALU_output == 0
            elif ins == 'BNE': 
                ALU_output = ALU_output != 0
            branch_logic_gate = main_con.Branch and ALU_output
            self.nextState.IF['PC'] = self.branch_MUX(PC + 4, PC + imm, branch_logic_gate)
            self.state.IF['PC'] = self.nextState.IF['PC']

        self.state.EX = {
            "nop": False, 
            "Read_data1": rs1_data_raw, 
            "Read_data2": rs2_data_raw, 
            "Imm": imm, 
            "Rs": rs1, 
            "Rt": rs2, 
            "Wrt_reg_addr": main_con.MemtoReg, 
            "rd_mem": main_con.MemRead,
            "wrt_mem": main_con.MemWrite, 
            "alu_op": main_con.ALUOp, 
            "wrt_enable": main_con.RegWrite, 
            }

        # 4. Access an operand in data memory (if necessary).
        lw_value = 0
        ALU_output_raw = int_to_bitstr(ALU_output)

        if main_con.MemWrite: 
            self.do_store(rs2_data_raw, ALU_output_raw)
        elif main_con.MemRead: 
            lw_value = self.do_load(ALU_output_raw)
        
        wb_value = self.WB_MUX(ALU_output_raw, lw_value, main_con.MemtoReg)

        self.state.MEM['ALUresult'] = ALU_output_raw
        self.state.MEM['Store_data'] = rs2
        self.state.MEM['Rs'] = rs1
        self.state.MEM['Rt'] = rs2
        self.state.MEM['Wrt_reg_addr'] = main_con.MemtoReg
        self.state.MEM['rd_mem'] = main_con.MemRead
        
        # 5. Write the result into a register (if necessary).
        if main_con.RegWrite: 
            self.do_write_back(rd, wb_value)

        self.state.WB['wrt_data'] = wb_value
        self.state.WB['Rs'] = rs1
        self.state.WB['Rt'] = rs2
        self.state.WB['Wrt_reg_addr'] = main_con.MemtoReg
        self.state.WB['wrt_enable'] = main_con.RegWrite

        if self.state.IF["nop"]:
            self.halted = True
        
        self.myRF.outputRF(self.cycle) # dump RF
        self.printState(self.state, self.cycle) # print states after executing cycle 0, cycle 1, cycle 2 ... 
            
        self.state = self.nextState #The end of the cycle and updates the current state with the values calculated in this cycle
        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-"*50+"\n", "State after executing cycle: " + str(cycle) + "\n"]
        for key in self.state.IF.keys(): 
            printstate.append("IF.{}: {}\n".format(key, state.IF[key]))
        printstate.append('\n')
        for key in state.ID.keys(): 
            printstate.append("ID.{}: {}\n".format(key, state.ID[key]))
        printstate.append('\n')
        for key in state.EX.keys(): 
            printstate.append("EX.{}: {}\n".format(key, state.EX[key]))
        printstate.append('\n')
        for key in state.MEM.keys(): 
            printstate.append("MEM.{}: {}\n".format(key, state.MEM[key]))
        printstate.append('\n')
        for key in state.WB.keys(): 
            printstate.append("WB.{}: {}\n".format(key, state.WB[key]))
        
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)

    def EX_MUX(self, rs2, imm, ALUSrc): 
        if ALUSrc: 
            return imm
        return rs2

    def branch_MUX(self, next, branch, logic_bit):
        if logic_bit: 
            return branch
        return next

    def do_store(self, rs2_data_raw, ALU_output): 
        self.ext_dmem.writeDataMem(ALU_output, rs2_data_raw)
    
    def do_load(self, ALU_output): 
        return self.ext_dmem.readDataMem(ALU_output)

    def WB_MUX(self, ALU_output, lw_value, MemtoReg): 
        if MemtoReg: 
            return lw_value
        return ALU_output

    def do_write_back(self, rd, wb_value): 
        self.myRF.writeRF(rd, wb_value)