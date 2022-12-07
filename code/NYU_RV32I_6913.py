import os
import argparse
from helper import *
from decoder import Parser, ImmGen
from ControlUnit import ControlUnit
from ALU import ALU_control, ALU

MemSize = 1000 # memory size, in reality, the memory size should be 2^32, but for this lab, for the space resaon, we keep it as this large number, but the memory is still 32-bit addressable.

class InsMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        
        with open(ioDir + "\\imem.txt") as im:
            self.IMem = [data.replace("\n", "") for data in im.readlines()]
            # print('Imem: {}'.format(self.IMem))
        while len(self.IMem) < MemSize: 
            self.IMem.append('00000000')

    def readInstr(self, ReadAddress):
        #read instruction memory
        #return 32 bit hex val
        instr = ''
        for i in range(4): 
            instr += self.IMem[ReadAddress + i]
        return instr
          
class DataMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        self.ioDir = ioDir
        with open(ioDir + "\\dmem.txt") as dm:
            self.DMem = [data.replace("\n", "") for data in dm.readlines()]
            # print('Dmem: {}'.format(self.DMem))
        while len(self.DMem) < MemSize: 
            self.DMem.append('00000000')

    def readDataMem(self, ReadAddress):
        #read data memory
        #return 32 bit hex val
        if isinstance(ReadAddress, str): 
            ReadAddress = bitstr_to_int(ReadAddress)

        data = ''
        for i in range(4): 
            data += self.DMem[ReadAddress + i]
        return data
        
    def writeDataMem(self, Address, WriteData):
        # write data into byte addressable memory
        if isinstance(WriteData, int): 
            WriteData = int_to_bitstr(WriteData)
        if isinstance(Address, str): 
            Address = bitstr_to_int(Address)

        parsedData = [WriteData[:8], WriteData[8:16], WriteData[16:24], WriteData[24:]]
        print('Before write: {}',format(self.DMem[Address:Address + 10]))
        for i in range(4): 
            self.DMem[Address + i] = parsedData[i]
        print('After write: {}',format(self.DMem[Address:Address + 10]))
                     
    def outputDataMem(self):
        resPath = self.ioDir + "\\" + self.id + "_DMEMResult.txt"
        with open(resPath, "w") as rp:
            rp.writelines([str(data) + "\n" for data in self.DMem])

class RegisterFile(object):
    def __init__(self, ioDir):
        self.outputFile = ioDir + "RFResult.txt"
        self.Registers = ['0'*32 for i in range(32)]
    
    def readRF(self, Reg_addr):
        # Read register files
        if isinstance(Reg_addr, str): 
            Reg_addr = bitstr_to_int(Reg_addr)

        return self.Registers[Reg_addr]
    
    def writeRF(self, Reg_addr, Wrt_reg_data):
        # Write register files
        if isinstance(Wrt_reg_data, int): 
            Wrt_reg_data = int_to_bitstr(Wrt_reg_data)

        self.Registers[Reg_addr] = Wrt_reg_data
         
    def outputRF(self, cycle):
        op = ["State of RF after executing cycle:" + str(cycle) + "\n"]
        op.extend([val+"\n" for val in self.Registers])
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.outputFile, perm) as file:
            file.writelines(op)

class State(object):
    def __init__(self):
        self.IF = {"nop": False, "PC": 0}
        self.ID = {"nop": False, "Instr": 0}
        self.EX = {"nop": False, "Read_data1": 0, "Read_data2": 0, "Imm": 0, "Rs1": 0, "Rs2": 0, "Rd": 0, "Branch": 0, "MemRead": 0, "MemtoReg": 0, "ALUOp": 0, 'MemWrite': 0, 'ALUSrc': 0, 'RegWrite': 0}
        self.MEM = {"nop": False, "ALUresult": 0, "Store_data": 0, "Rs1": 0, "Rs2": 0, 'Rd': 0, "MemtoReg": 0, "MemRead": 0, "MemWrite": 0, "RegWrite": 0}
        self.WB = {"nop": False, "Write_data": 0, "Rs1": 0, "Rs2": 0, "Rd": 0, "RegWrite": 0}

class Core(object):
    def __init__(self, ioDir, imem, dmem):
        self.myRF = RegisterFile(ioDir)
        self.cycle = 0
        self.halted = False
        self.ioDir = ioDir
        self.state = State()
        self.nextState = State()
        self.ext_imem = imem
        self.ext_dmem = dmem

    def assign_value(self, ioDir, imem, dmem):
        self.ioDir = ioDir
        self.ext_imem = imem
        self.ext_dmem = dmem

class SingleStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(SingleStageCore, self).__init__(ioDir + "\\SS_", imem, dmem)
        self.opFilePath = ioDir + "\\StateResult_SS.txt"

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
        rs1_data_raw = self.myRF.readRF(rs1)
        rs2_data_raw = self.myRF.readRF(rs2)
        if type == 'J': 
            rs1_data_raw = int_to_bitstr(PC)
            rs2_data_raw = int_to_bitstr(4)
        print('{}\t{}\tx{}\tx{}\tx{}\t{}'.format(self.cycle, ins, rd, rs1, rs2, imm))

        if type == 'H': 
            self.state.IF['nop'] = True
            self.state.ID['nop'] = True
            self.state.EX['nop'] = True
            self.state.MEM['nop'] = True
            self.state.WB['nop'] = True
            
        self.state.ID['Instr'] = instr

        # 3. Execute the operation or calculate an address.

        main_con = ControlUnit(type, ins)
        ALU_con = ALU_control(opcode, funct7, funct3, main_con.ALUOp)
        input2_raw = self.EX_MUX(rs2_data_raw, imm_raw, main_con.ALUSrc)

        ALU_output_raw = ALU(ALU_con, ins, rs1_data_raw, input2_raw)

        # Branch
        ALU_zero = 0
        if ins == 'BEQ': 
            ALU_zero = ALU_output_raw == 0
        elif ins == 'BNE': 
            ALU_zero = ALU_output_raw != 0
        PCsrc = main_con.Branch and ALU_zero
        self.nextState.IF['PC'] = self.branch_MUX(PC + 4, PC + imm, PCsrc)
        self.state.IF['PC'] = self.nextState.IF['PC']

        self.state.EX['Read_data1'] = rs1_data_raw
        self.state.EX['Read_data2'] = rs2_data_raw
        self.state.EX['Imm'] = imm_raw
        self.state.EX['Rs1'] = rs1
        self.state.EX['Rs2'] = rs2
        self.state.EX['Rd'] = rd
        self.state.EX['Branch'] = main_con.Branch
        self.state.EX['MemRead'] = main_con.MemRead
        self.state.EX['MemtoReg'] = main_con.MemtoReg
        self.state.EX['ALUOp'] = main_con.ALUOp
        self.state.EX['MemWrite'] = main_con.MemWrite
        self.state.EX['ALUSrc'] = main_con.ALUSrc
        self.state.EX['RegWrite'] = main_con.RegWrite

        # 4. Access an operand in data memory (if necessary).
        lw_value = 0

        if main_con.MemWrite: 
            self.do_store(rs2_data_raw, ALU_output_raw)
        elif main_con.MemRead: 
            lw_value = self.do_load(ALU_output_raw)
        
        wb_value = self.WB_MUX(ALU_output_raw, lw_value, main_con.MemtoReg)

        self.state.MEM['ALUresult'] = ALU_output_raw
        self.state.MEM['Store_data'] = rs2
        self.state.MEM['Rs1'] = rs1
        self.state.MEM['Rs2'] = rs2
        self.state.MEM['Rd'] = rd
        self.state.MEM['MemtoReg'] = main_con.MemtoReg
        self.state.MEM['MemRead'] = main_con.MemRead
        self.state.MEM['MemWrite'] = main_con.MemWrite
        self.state.MEM['RegWrite'] = main_con.RegWrite
        
        # 5. Write the result into a register (if necessary).
        if main_con.RegWrite: 
            self.do_write_back(rd, wb_value)

        self.state.WB['Write_data'] = wb_value
        self.state.WB['Rs1'] = rs1
        self.state.WB['Rs2'] = rs2
        self.state.WB['Rd'] = rd
        self.state.WB['RegWrite'] = main_con.RegWrite

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

    def do_store(self, rs2_data_raw, ALU_output_raw): 
        self.ext_dmem.writeDataMem(ALU_output_raw, rs2_data_raw)
    
    def do_load(self, ALU_output_raw): 
        return self.ext_dmem.readDataMem(ALU_output_raw)

    def WB_MUX(self, ALU_output_raw, lw_value, MemtoReg): 
        if MemtoReg: 
            return lw_value
        return ALU_output_raw

    def do_write_back(self, rd, wb_value): 
        self.myRF.writeRF(rd, wb_value)

class FiveStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(FiveStageCore, self).__init__(ioDir + "\\FS_", imem, dmem)
        self.opFilePath = ioDir + "\\StateResult_FS.txt"

    def step(self):
        # Your implementation
        # --------------------- WB stage ---------------------
        self.WB(MEM_WB, WB_con)
        
        # --------------------- MEM stage --------------------
        PC_imm, PCsrc, MEM_WB = self.MEM(EX_MEM, MEM_con)

        self.state.WB['Write_data'] = wb_value
        self.state.WB['Rs1'] = rs1
        self.state.WB['Rs2'] = rs2
        self.state.WB['Rd'] = rd
        self.state.WB['RegWrite'] = main_con.RegWrite
        

        # --------------------- EX stage ---------------------
        rs1 = self.state.EX['Rs1']
        rs2 = self.state.EX['Rs2']
        rd_EX = self.state.MEM['Wrt_']
        forwarding = self.forwarding_unit(rs1, rs2, )
        PC_imm, ALU_zero, ALU_output_raw, rs2_data_raw, rd = self.EX(ID_EX, EX_con, opcode, funct7, funct3, forwarding)

        self.state.MEM['ALUresult'] = ALU_output_raw
        self.state.MEM['Store_data'] = rs2
        self.state.MEM['Rs1'] = rs1
        self.state.MEM['Rs2'] = rs2
        self.state.MEM['Rd'] = rd
        self.state.MEM['MemtoReg'] = main_con.MemtoReg
        self.state.MEM['MemRead'] = main_con.MemRead
        self.state.MEM['MemWrite'] = main_con.MemWrite
        self.state.MEM['RegWrite'] = main_con.RegWrite

        
        # --------------------- ID stage ---------------------
        main_con = ControlUnit(type, ins)
        EX_con = (main_con.ALUSrc, main_con.ALUOp)
        MEM_con = (main_con.Branch, main_con.MemRead, main_con.MemWrite)
        WB_con = (main_con.RegWrite, main_con.MemtoReg)
        PC, rs1_data_raw, rs2_data_raw, imm_raw, rd = self.ID(IF_ID)
        
        self.state.EX['Read_data1'] = rs1_data_raw
        self.state.EX['Read_data2'] = rs2_data_raw
        self.state.EX['Imm'] = imm_raw
        self.state.EX['Rs1'] = rs1
        self.state.EX['Rs2'] = rs2
        self.state.EX['Rd'] = rd
        self.state.EX['Branch'] = main_con.Branch
        self.state.EX['MemRead'] = main_con.MemRead
        self.state.EX['MemtoReg'] = main_con.MemtoReg
        self.state.EX['ALUOp'] = main_con.ALUOp
        self.state.EX['MemWrite'] = main_con.MemWrite
        self.state.EX['ALUSrc'] = main_con.ALUSrc
        self.state.EX['RegWrite'] = main_con.RegWrite
        

        # --------------------- IF stage ---------------------
        IF_ID = self.IF(PC_imm, PCsrc)
        PC, instr = IF_ID
        self.state.ID['Instr'] = instr


        self.halted = True
        if self.state.IF["nop"] and self.state.ID["nop"] and self.state.EX["nop"] and self.state.MEM["nop"] and self.state.WB["nop"]:
            self.halted = True
        
        self.myRF.outputRF(self.cycle) # dump RF
        self.printState(self.nextState, self.cycle) # print states after executing cycle 0, cycle 1, cycle 2 ... 
        
        self.state = self.nextState #The end of the cycle and updates the current state with the values calculated in this cycle
        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-"*70+"\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.extend(["IF." + key + ": " + str(val) + "\n" for key, val in state.IF.items()])
        printstate.extend(["ID." + key + ": " + str(val) + "\n" for key, val in state.ID.items()])
        printstate.extend(["EX." + key + ": " + str(val) + "\n" for key, val in state.EX.items()])
        printstate.extend(["MEM." + key + ": " + str(val) + "\n" for key, val in state.MEM.items()])
        printstate.extend(["WB." + key + ": " + str(val) + "\n" for key, val in state.WB.items()])

        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)
    

    def WB(self, MEM_WB, WB_con):
        wb_value, ALU_output_raw, rd = MEM_WB
        RegWrite, MemtoReg = WB_con
        wb_value = self.WB_MUX(ALU_output_raw, lw_value, MemtoReg)
        if RegWrite: 
            self.do_write_back(rd, wb_value)

        self.state.WB['wrt_data'] = wb_value
        self.state.WB['Rs1'] = rs1
        self.state.WB['Rs2'] = rs2
        self.state.WB['Wrt_reg_addr'] = MemtoReg
        self.state.WB['wrt_enable'] = RegWrite


    def MEM(self, EX_MEM, MEM_con):
        PC_imm, ALU_zero, ALU_output_raw, rs2_data_raw, rd = EX_MEM
        Branch, MemRead, MemWrite = MEM_con
        ALU_output_raw = int_to_bitstr(ALU_output_raw)
        PCsrc = Branch and ALU_zero

        lw_value = 0
        if MemWrite: 
            self.do_store(rs2_data_raw, ALU_output_raw)
        elif MemRead: 
            lw_value = self.do_load(ALU_output_raw)


        self.state.MEM['ALUresult'] = ALU_output_raw
        self.state.MEM['Store_data'] = rs2
        self.state.MEM['Rs1'] = rs1
        self.state.MEM['Rs2'] = rs2
        self.state.MEM['Rd'] = rd
        self.state.MEM['MemtoReg'] = main_con.MemtoReg
        self.state.MEM['MemRead'] = main_con.MemRead
        self.state.MEM['MemWrite'] = main_con.MemWrite
        self.state.MEM['RegWrite'] = main_con.RegWrite

        MEM_WB = (wb_value, ALU_output_raw, rd)
        return (PC_imm, PCsrc, MEM_WB)

    def EX(self, ID_EX, EX_con, opcode, funct7, funct3, forwarding): 
        forwardA, forwardB = forwarding

        ALUSrc, ALUOp = EX_con
        PC, rs1_data_raw, rs2_data_raw, imm_raw, rd = ID_EX

        ALU_con = ALU_control(opcode, funct7, funct3, ALUOp)
        input1_raw = self.EX_MUX_A(rs1_data_raw, forwardA)
        inputB_raw = self.EX_MUX_B(rs2_data_raw, forwardB)
        input2_raw = self.EX_MUX_2(inputB_raw, imm_raw)

        ALU_output_raw = ALU(ALU_con, ins, input1_raw, input2_raw)

        imm = bitstr_to_int(imm_raw)
        PC_imm = PC + imm
        # Branch
        if ins == 'BEQ': 
            ALU_zero = ALU_zero == 0
        elif ins == 'BNE': 
            ALU_zero = ALU_zero != 0
        
        EX_MEM = (PC_imm, ALU_zero, ALU_output_raw, rs2_data_raw, rd)
        return EX_MEM

    def ID(self, IF_ID): 
        PC, instr = IF_ID
        parser = Parser(instr)
        funct7 = parser.funct7
        funct3 = parser.funct3
        opcode = parser.opcode
        type, ins, rs2_raw, rs1_raw, rd_raw = parser.parse()
        imm_raw = ImmGen(instr, type)
        rs2 = int(rs2_raw, 2)
        rs1 = int(rs1_raw, 2)
        rd = int(rd_raw, 2)
        rs1_data_raw = self.myRF.readRF(rs1)
        rs2_data_raw = self.myRF.readRF(rs2)
        if type == 'J': 
            rs1_data_raw = int_to_bitstr(PC)
            rs2_data_raw = int_to_bitstr(4)
        print('{}\t{}\tx{}\tx{}\tx{}\t{}'.format(self.cycle, ins, rd, rs1, rs2, bitstr_to_int(imm_raw)))

        
        if type == 'H': 
            self.state.ID['nop'] = True
            
        self.state.ID['Instr'] = instr
        ID_EX = (PC, rs1_data_raw, rs2_data_raw, imm_raw, rd)
        return ID_EX

    def IF(self, PC_imm, PCsrc):
        PC = self.state.IF['PC']
        instr = self.ext_imem.readInstr(PC)

        self.nextState.IF['PC'] = self.branch_MUX(PC + 4, PC_imm, PCsrc)
        self.state.IF['PC'] = self.nextState.IF['PC']

        IF_ID = (PC, instr)
        return IF_ID
    
    def EX_MUX_A(self, rs1, forwardA): 
        if forwardA == 0b00: 
            return rs1
        elif forwardA == 0b10: 
            return self.state.MEM['ALUresult']
        elif forwardA == 0b01: 
            return self.state.WB['Write_data']

    def EX_MUX_B(self, rs2, forwardB): 
        if forwardB == 0b00: 
            return rs2
        elif forwardB == 0b10: 
            return self.state.MEM['ALUresult']
        elif forwardB == 0b01: 
            return self.state.WB['Write_data']
    
    def EX_MUX_2(self, inputB, imm_raw):
        if self.state.EX['ALUSrc']:
            return imm_raw
        return inputB

    def PC_MUX(self, PC_4, PC_imm, control): 
        pass

    def hazard_detection_unit(self): 
        ID_EX = self.state.EX
        IF_ID = self.state.ID
        if ID_EX['MemRead'] and ((ID_EX['rd'] == IF_ID['rs1']) or (ID_EX['rd'] == IF_ID['rs2'])): 
            self.state.ID['nop'] = True
            return True
        return False
    
    def forwarding_unit(self): 
        forwardA = 0
        forwardB = 0
        EX_MEM = self.state.MEM
        MEM_WB = self.state.WB
        ID_EX = self.state.EX

        if (EX_MEM['RegWrite'] and (EX_MEM['rd'] != 0) and (EX_MEM['rd'] == ID_EX['rs1'])): 
            forwardA = 10

        if (EX_MEM['RegWrite'] and (EX_MEM['rd'] != 0) and (EX_MEM['rd'] == ID_EX['rs2'])):
            forwardB = 10

        if MEM_WB['RegWrite'] and (MEM_WB['rd'] != 0) and not(EX_MEM['RegWrite'] and (EX_MEM['rd'] != 0) and (EX_MEM['rd'] == ID_EX['rs1'])) and (MEM_WB['rd'] == ID_EX['rs1']):
            forwardA = 0b01

        if (MEM_WB['RegWrite'] and (MEM_WB['rd'] != 0) and not(EX_MEM['RegWrite'] and (EX_MEM['rd'] != 0) and (EX_MEM['rd'] == ID_EX['rs2'])) and (MEM_WB['rd'] == ID_EX['rs2'])): 
            forwardB = 0b01
        
        return (forwardA, forwardB)

if __name__ == "__main__":
     
    #parse arguments for input file location
    parser = argparse.ArgumentParser(description='RV32I processor')
    parser.add_argument('--iodir', default="", type=str, help='Directory containing the input files.')
    args = parser.parse_args()

    test_case = 3
    test_path = '\\6913_ProjA_TC\\TC' + str(test_case)
    ioDir = os.path.abspath(args.iodir) + test_path
    print("IO Directory:", ioDir)

    imem = InsMem("Imem", ioDir)
    dmem_ss = DataMem("SS", ioDir)
    dmem_fs = DataMem("FS", ioDir)
    
    ssCore = SingleStageCore(ioDir, imem, dmem_ss)
    fsCore = FiveStageCore(ioDir, imem, dmem_fs)

    while(True):
        if not ssCore.halted:
            ssCore.step()
        
        # if not fsCore.halted:
        #     fsCore.step()

        # if ssCore.halted and fsCore.halted:
        #     break
        if ssCore.halted: 
            break
    
    # dump SS and FS data mem.
    dmem_ss.outputDataMem()
    dmem_fs.outputDataMem()