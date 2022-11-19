
import time
# prints out the command and load output associated to it
def cmd8500(cmd , ser):
    # print("Command: ", hex(cmd[2]))
    # printbuff(cmd)
    ser.write(cmd)
    # time.sleep(0.2)
    resp = ser.readline(26)
    print("Resp: ")
    printbuff(resp)
    return resp
    
def printbuff(b):
    r=""
    for s in range(len(b)):
        r+=" "
        r+=hex(b[s]).replace('0x','')
    print(r)

# calculates the checksum
def csum(thing):
    sum = 0
    for i in range(len(thing)):
        sum+=thing[i]
    return 0xFF&sum

    