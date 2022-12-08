import string
import binascii
import time

# rotateby: -12

# prints out the command and load output associated to it
# returns a list of length 26
def cmd8500(cmd , ser):
    # import resetload
    print("Command: ", hex(cmd[2]))
    print(list(cmd))
    ser.write(cmd)
    # time.sleep(0.2)
    resp = ser.readline(26)
    print("Resp: ")
    # terminate if response is less than expected
    # if (len(resp) < 26):
    #     resetload.resetLoad(cmd, ser)
    printbuff(resp)

    resp_list = list(resp)
    if (resp_list[0] != 170): # if byte 0xaa is not at start, find it and put it at start
        start_index = resp_list.index(170) if 170 in resp_list else -1
        if start_index == -1: # probably means less than 26 bytes sent
            return resp_list    
        rotated_list = rotate(resp_list, start_index)
        print(rotated_list)
        return rotated_list
    else:
        print(resp_list)
        return resp_list




def rotate(l, n):
    return l[n:] + l[:n]

# param[in] resp_list: a 4-length list of ints in litte-endian ordering 
#                      received from serial response
# return: integer representation of a little_endian 4-byte hex sequence
def get_big_hex(resp_list):
    # assert(len(resp_list) == 4)
    if len(resp_list) < 4:
        print("HEX ENDY LEN LESS THAN 4; IS: {}", len(resp_list))
    byte1 = "0x{:02x}".format(resp_list[3])
    byte2 = "{:02x}".format(resp_list[2])
    byte3 = "{:02x}".format(resp_list[1])
    byte4 = "{:02x}".format(resp_list[0])
    print("individual list items look like: {} {} {} {}", byte1, byte2, byte3, byte4)
    big_endy = byte1 + byte2 + byte3 + byte4
    print("concatenated bytes: {}", big_endy)
    print("in int format: {}", int(big_endy, 16))
    return int(big_endy, 16)
    # byte1 = byte1.to_bytes(1, 'little')
    # byte2 = byte2.to_bytes(1, 'little')
    # byte3 = byte3.to_bytes(1, 'little')
    # byte4 = byte4.to_bytes(1, 'little')
    # big_endy = 
    print(byte1, ",", byte2, ",", byte3, ",", byte4)
    
    print(bytes.tohex(byte1))
    


# calculates the checksum
def csum(thing):
    sum = 0
    for i in range(len(thing)):
        sum+=thing[i]
    return 0xFF&sum

def printbuff(b):
    r=""
    for s in range(len(b)):
        r+=" "
        r+=hex(b[s]).replace('0x','')
    print(r)
    

# returns the voltage read as an int (in units of mV)
def readVoltage(resp):
    
    # voltage = "0x"
    # # 01 23 45 [67 89 1011 1213]
    
    # for x in range (6, 2, -1):
    #     voltage = voltage + hex(resp[x]).replace('0x','')
    # print("before:", voltage)
    # voltage = int(voltage, 16)
    # print("after:", voltage)
    # # print("voltage = ", voltage)
    # return voltage
    voltage_list = resp[3:7]
    print("V: {}", voltage_list)
    voltage = get_big_hex(voltage_list)
    return voltage
# returns the current read as an int (in units of mA)
# param[in] resp: a list of integers of length 26
def readCurrent(resp):
    # current = "0x"
    # # 01 23 45 67 89 1011 1213 [1415 1617 1819 2021]
    # for x in range (10, 6, -1):
    #     current = current + hex(resp[x]).replace('0x','')
    # print("before: ", current)
    # current = int(current, 16)
    # print("after: ", current)
    # # print("current = ", current)
    # return current
    current_list = resp[7:11]
    print("C: {}", current_list)
    current = get_big_hex(current_list)
    return current

# Read terminal voltage and current 
# returns an array of format [imtestamp]
def readVC(cmd, ser):
    vcData = []
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x5f
    cmd[25]=csum(cmd)
    resp = cmd8500(cmd, ser) # resp is a list of length 26
    while (len(resp) < 26): # keep attempting to read if length is less than 26
        resp = cmd8500(cmd, ser) # potential infinite loop here watch out
        print("[readVC] stuck at index out of range") 

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


