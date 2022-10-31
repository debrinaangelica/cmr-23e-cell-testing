
import bk8500functions

# Convert decimal to little endian hex


# Read terminal voltage and current 
def readVC(cmd, sp):
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x5f
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd,sp)
    # Response structure: 
    # bits 3-6 terminal voltage un units of 1 mV
    # bits 7-10 terminal current in units of 0.1 mA