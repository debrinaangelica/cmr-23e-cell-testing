
import bk8500functions

# Convert little endian hex of voltage to decimal
def readVoltage(resp):
    voltage = 0
    # 01 23 45 [67 89 1011 1213]
    # gets the hex representation of the output in big endian form
    for x in range (12, 4, -2):
        voltage.append(resp[x:x+2])
    voltage = int(voltage)
    return voltage

def readCurrent(resp):
    current = ""
    # 01 23 45 67 89 1011 1213 [1415 1617 1819 2021]
    # gets the hex representation of the output in big endian form
    for x in range (20, 12, -2):
        current.append(resp[x:x+2])
    current = int(current)
    return current

# Read terminal voltage and current 
def readVC(cmd, ser):
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x5f
    cmd[25]=bk8500functions.csum(cmd)
    # parse the load's output to get the voltage only
    resp = ser.readline(26)
    print(readCurrent(resp), '\n')
    print(readVoltage(resp), '\n')



    # bk8500functions.cmd8500(cmd, ser)
    # Response structure: 
    # bits 3-6 terminal voltage in units of 1 mV
    # bits 7-10 terminal current in units of 0.1 mA