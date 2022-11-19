import string


# prints out the command and load output associated to it
# returns a list of length 26
def cmd8500(cmd , ser):
    import resetload
    print("Command: ", hex(cmd[2]))
    print(list(cmd))
    ser.write(cmd)
    resp = ser.readline(26)
    print("Resp: ")
    # safety check
    if (len(resp) < 26):
        resetload.resetLoad(cmd, ser)
    resp = list(resp)
    return resp

# calculates the checksum
def csum(thing):
    sum = 0
    for i in range(len(thing)):
        sum+=thing[i]
    return 0xFF&sum

    

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
    cmd[25]=csum(cmd)
    resp = cmd8500(cmd, ser)
    
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
    cmd[25]=csum(cmd)
    resp = cmd8500(cmd, ser)

    # extract the voltage data from response (units of V)
    voltage = float(readVoltage(resp)) / 1000

    # check voltage cutoff
    if (voltage < 3):
        return -1
    else:
        return 0


