import os
import argparse
from helper import *
from decoder import Parser, ImmGen
from ControlUnit import ControlUnit
from Conditional import Conditional
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
        self.EX = {"nop": False, "Read_data1": 0, "Read_data2": 0, "Imm": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "is_I_type": False, "rd_mem": 0, 
                   "wrt_mem": 0, "alu_op": 0, "wrt_enable": 0}
        self.MEM = {"nop": False, "ALUresult": 0, "Store_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "rd_mem": 0, 
                   "wrt_mem": 0, "wrt_enable": 0}
        self.WB = {"nop": False, "Wrt_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "wrt_enable": 0}

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

class FiveStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(FiveStageCore, self).__init__(ioDir + "\\FS_", imem, dmem)
        self.opFilePath = ioDir + "\\StateResult_FS.txt"

    def step(self):
        # Your implementation
        # --------------------- IF stage ---------------------
        
        
        
        # --------------------- ID stage --------------------
        
        
        
        # --------------------- EX stage ---------------------
        
        
        
        # --------------------- MEM stage ---------------------
        
        
        
        # --------------------- WB stage ---------------------
        
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
        
        if not fsCore.halted:
            fsCore.step()

        if ssCore.halted and fsCore.halted:
            break
    
    # dump SS and FS data mem.
    dmem_ss.outputDataMem()
    dmem_fs.outputDataMem()