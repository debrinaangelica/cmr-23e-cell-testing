

# prints out the command and load output associated to it
def cmd8500(cmd , ser):
    print("Command: ", hex(cmd[2]))
    printbuff(cmd)
    ser.write(cmd)
    resp = ser.readline(26)
    print("Resp: ")
    printbuff(resp)
    

# ORIGINAL PRINTBUFF: prints the serial output into a readable little-endian hex format
#   hex(x) converts integer x to hex form
#   r+=" " puts a space in between each hex 
# def printbuff(b):
#     r=""
#     for s in range(len(b)):
#         r+=" "
#         r+=hex(b[s]).replace('0x','')
#     print(r)

# printbuff, but what if we don't convert the string into a hex?
def printbuff(b):
    print(b)

# calculates the checksum
def csum(thing):
    sum = 0
    for i in range(len(thing)):
        sum+=thing[i]
    return 0xFF&sum