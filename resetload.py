import serial
import bk8500functions

length_packet = 26
num_test_cycles = 10

def resetLoad(cmd, sp):
    # Reset constant current to 0A
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x2A
    cmd[3]=0x00 # LSB of current value 15A = 160000*0.1mA = 27100
    cmd[4]=0x00
    cmd[5]=0x00
    cmd[6]=0x00 # MSB
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd,sp)

# Reset constant voltage to 0A
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x2C
    cmd[3]=0x00 # LSB of current value 15A = 160000*0.1mA = 27100
    cmd[4]=0x00
    cmd[5]=0x00
    cmd[6]=0x00 # MSB
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd,sp)

# Turn OFF the load
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x21
    cmd[3]=0x00
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd, sp)

    print("LOAD RESET")


def main():
    sp = serial.Serial()
    sp.setBaudrate = 9600
    sp.port = 'COM6'
    sp.open()
    print(sp)

    cmd=[0]*26
    resetLoad(cmd, sp)

main()