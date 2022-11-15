import sys 
sys.path.append("..") 
from NYU_RV32I_6913 import InsMem, DataMem, RegisterFile
import os
import argparse
def test_IM(ioDir):
    IM = InsMem(0, ioDir)

    # Read test
    assert len(IM.readInstr(5)) == 32
    assert IM.readInstr(5) == '00000010000000000000010010001100'
    assert IM.readInstr(10) == '00000000000000001000110000000100'

    try: 
        IM.readInstr(40)
    except:
        pass
    else: 
        raise Exception

def test_DM(ioDir): 
    DM = DataMem(0, ioDir)

    # Read test
    assert len(DM.readDataMem(3)) == 32
    assert DM.readDataMem(3) == '11111111011111111111111111111111'

    try: 
        DM.readDataMem(40)
    except:
        pass
    else: 
        raise Exception

    # Write test
    DM.writeDataMem(4, 332211)
    assert len(DM.readDataMem(3)) == 32
    assert DM.readDataMem(3) == '11111111' + '0000000000000' + '10100010001'

    try: 
        DM.writeDataMem(40, 12)
    except:
        pass
    else: 
        raise Exception

def test_RF(ioDir): 
    RF = RegisterFile(ioDir)

    # Initialization test
    for i in range(32): 
        assert RF.Registers[i] == 0

    # Read test
    for i in range(32): 
        assert RF.readRF(i) == 0
    try: 
        RF.readRF(33)
    except:
        pass
    else: 
        raise Exception

    # Write test
    RF.writeRF(3, 12)
    assert RF.readRF(3) == 12
    RF.writeRF(30, -190)
    assert RF.readRF(30) == -190
    try: 
        RF.writeRF(40, 10)
    except:
        pass
    else: 
        raise Exception



parser = argparse.ArgumentParser(description='RV32I processor')
parser.add_argument('--iodir', default="", type=str, help='Directory containing the input files.')
args = parser.parse_args()
ioDir = os.path.abspath(args.iodir)

test_IM(ioDir)
test_DM(ioDir)
test_RF(ioDir)
print('Test pass!')