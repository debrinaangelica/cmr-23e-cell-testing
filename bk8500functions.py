# copy pasted original


def cmd8500(cmd , ser):
    import resetload
    print("Command: ", hex(cmd[2]))
    printbuff(cmd)
    ser.write(cmd)
    resp = ser.read(26)
    #print("Resp: ")
    printbuff(resp)

    # safety check
    if (len(resp) < 26):
        resetload.resetLoad(cmd, ser)
    
def printbuff(b):
    r=""
    for s in range(len(b)):
        r+=" "
        r+=hex(b[s]).replace('0x','')
    print(r)

def csum(thing):
    sum = 0
    for i in range(len(thing)):
        sum+=thing[i]
    return 0xFF&sum