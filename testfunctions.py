
import bk8500functions
import string

# returns the voltage read as an int (in units of mV)
def readVoltage(resp):
    
    voltage = "0x"
    # 01 23 45 [67 89 1011 1213]
    
    for x in range (6, 2, -1):
        voltage = voltage + hex(resp[x]).replace('0x','')
    print("before:", voltage)
    voltage = int(voltage, 16)
    print("after:", voltage)
    # print("voltage = ", voltage)
    return voltage

# returns the current read as an int (in units of mA)
def readCurrent(resp):
    current = "0x"
    # 01 23 45 67 89 1011 1213 [1415 1617 1819 2021]
    for x in range (10, 6, -1):
        current = current + hex(resp[x]).replace('0x','')
    print("before: ", current)
    current = int(current, 16)
    print("after: ", current)
    # print("current = ", current)
    return current    

# Read terminal voltage and current 
# returns an array of format [imtestamp]
def readVC(cmd, ser):
    vcData = []
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x5f
    cmd[25]=bk8500functions.csum(cmd)
    resp = bk8500functions.cmd8500(cmd, ser)
    
    # extract the current data from response (units of A)
    current = float(readCurrent(resp)) / 10000

    # extract the voltage data from response (units of V)
    voltage = float(readVoltage(resp)) / 1000

    # print extracted data
    print("current: ", current, "  voltage: ", voltage)
    
    # format the data into an array to return
    vcData.append(voltage)
    vcData.append(current)
    return vcData

    # bk8500functions.cmd8500(cmd, ser)
    # Response structure: 
    # bits 3-6 terminal voltage in units of 0.1 mV
    # bits 7-10 terminal current in units of 0.1 mA

# Checks cell voltage at 0A. 
# Ends testing when voltage is less than 3V
def checkCutoffVoltage(cmd, ser):
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x5f
    cmd[25]=bk8500functions.csum(cmd)
    resp = bk8500functions.cmd8500(cmd, ser)

    # extract the voltage data from response (units of V)
    voltage = float(readVoltage(resp)) / 1000

    # check voltage cutoff
    if (voltage < 3):
        return -1
    else:
        return 0


def DecodeInteger(self, str):
    # '''Construct an integer from the little endian string. 1, 2, and 4 byte 
    # strings are the only ones allowed.
    # '''
    assert(len(str) == 1 or len(str) == 2 or len(str) == 4)
    n  = ord(str[0])
    if len(str) >= 2:
        n += (ord(str[1]) << 8)
        if len(str) == 4:
            n += (ord(str[2]) << 16)
            n += (ord(str[3]) << 24)
    return n

def GetInputValues(self):
    # '''Returns voltage in V, current in A, and power in W, op_state byte,
    # and demand_state byte.
    # '''
    cmd = self.StartCommand(0x5F)
    cmd += self.Reserved(3)
    cmd += chr(self.CalculateChecksum(cmd))
    assert(self.CommandProperlyFormed(cmd))
    response = self.SendCommand(cmd)
    self.PrintCommandAndResponse(cmd, response, "Get input values")
    voltage = self.DecodeInteger(response[3:7])/self.convert_voltage
    current = self.DecodeInteger(response[7:11])/self.convert_current
    power   = self.DecodeInteger(response[11:15])/self.convert_power
    op_state = hex(self.DecodeInteger(response[15]))
    demand_state = hex(self.DecodeInteger(response[16:18]))
    s = [str(voltage) + " V", str(current) + " A", str(power) + " W", str(op_state), str(demand_state)]
    return join(s, "\t")