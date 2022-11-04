
import bk8500functions

# Convert little endian hex of voltage to decimal
# def readVoltage(resp):
#     voltage = 0
#     # 01 23 45 [67 89 1011 1213]
#     # gets the hex representation of the output in big endian form
#     for x in range (12, 4, -2):
#         voltage.append(resp[x:x+2])
#     voltage = int(voltage)
#     return voltage

# returns the voltage read as an int (in units of mV)
def readVoltage(resp):
    voltage = "0x"
    # 01 23 45 [67 89 1011 1213]
    for x in range (6, 2, -1):
        voltage = voltage + hex(resp[x]).replace('0x','')
    voltage = int(voltage, 16)
    print("voltage = ", voltage)
    return voltage

# returns the current read as an int (in units of mA)
def readCurrent(resp):
    current = "0x"
    # 01 23 45 67 89 1011 1213 [1415 1617 1819 2021]
    for x in range (10, 6, -1):
        current = current + hex(resp[x]).replace('0x','')
    current = int(current, 16)
    print("current = ", current)
    return current    

# Read terminal voltage and current 
# returns an array of format [imtestamp]
def readVC(cmd, ser):
    vcData = []
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x5f
    cmd[25]=bk8500functions.csum(cmd)

    # write our command to serial     
    ser.write(cmd)
    # get serial response
    resp = ser.readline(26)
    # extract the current data from response
    current = readCurrent(resp)
    # extract the voltage data from response
    voltage = readVoltage(resp)
    # print extracted data
    print("current: ", current, "  voltage: ", voltage)
    # format the data into an array to return
    vcData.append(current)
    vcData.append(voltage)
    return vcData

# append time
# readVC
# append readVC
# print
# 


    # bk8500functions.cmd8500(cmd, ser)
    # Response structure: 
    # bits 3-6 terminal voltage in units of 1 mV
    # bits 7-10 terminal current in units of 0.1 mA