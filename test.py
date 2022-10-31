# DO WE WANT TO REST 100s AFTER DOING THE 0.5A - 15A SWITCH
# TODO: TEST IF FOR I IN RANGE ACTUALLY RUNS RANGE NUMBER OF TIMES
# TODO: TEST IF CURRENT LIMIT ACTUALLY LIMITS THE CURRENT
# TODO: FIND A WAY TO STORE DATA IN CSV FILE AND MARK TIMESTAMPS IN PARALLEL

# List of currents in hex
# 3A = 0x7530
# 0.5A = 0x1388
# 10A = 0x186A0
# 15A = 0x249F0

import signal
import serial
import time
import csv
import sys
import bk8500functions
import testfunctions
import resetload

# GLOBAL VARIABLES
length_packet = 26
num_test_cycles = 10
sp = serial.Serial()
sp.setBaudrate = 9600
sp.port = 'COM6'
cmd=[0]*26
# END OF GLOBAL VARIABLES


with open('testdata.csv', 'w', newline='') as csvfile:   # unsure what this newline does
    fieldnames = ['timestamp', 'voltage', 'current']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # .writer or .DictWriter ?
    writer.writeheader()

def abort(signum, frame):
    resetload.resetLoad(cmd, sp)
    sys.terminate()

def main():
    sp.open()
    print(sp)
    signal.signal(signal.SIGINT, abort) 
    
## Construct a set to remote command
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x20
    cmd[3]=0x01
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd, sp)
    
### Turn ON the load
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x21
    cmd[3]=0x01
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd, sp)

#Set voltage limit to __V
#     cmd=[0]*26
#     cmd[0]=0xAA
#     cmd[2]=0x22
#     cmd[3]=0x00 # LSB of voltage value
#     cmd[4]=0x00
#     cmd[4]=0x00
#     cmd[4]=0x00 # MSB
#     cmd[25]=bk8500functions.csum(cmd)
#     bk8500functions.cmd8500(cmd,sp) 

# Set current limit to 16A
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x24
    cmd[3]=0x00 # LSB of current value 16A = 160000*0.1mA = 27100
    cmd[4]=0x71
    cmd[5]=0x02
    cmd[6]=0x00 # MSB
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd,sp)

    for i in range(num_test_cycles):
    # Set constant current of 0.5A = 0x1388 for 10 seconds
        cmd=[0]*26
        cmd[0]=0xAA
        cmd[2]=0x2A
        cmd[3]=0x88 # LSB of current value 
        cmd[4]=0x13
        cmd[5]=0x00
        cmd[6]=0x00 # MSB
        cmd[25]=bk8500functions.csum(cmd)
        bk8500functions.cmd8500(cmd,sp)

        print("read data 0.5A:")
    # Continuously collect votlage and current data for 10 seconds
        t_readdata = time.time() + 10
        while time.time() < t_readdata:
            testfunctions.readVC(cmd, sp)
            
    # Set constant current of 15A = 0x249F0 for 0.5 seconds
        cmd=[0]*26
        cmd[0]=0xAA
        cmd[2]=0x2A
        cmd[3]=0xF0 # LSB of current value 15A = 160000*0.1mA = 249F0
        cmd[4]=0x49
        cmd[5]=0x02
        cmd[6]=0x00 # MSB
        cmd[25]=bk8500functions.csum(cmd)
        bk8500functions.cmd8500(cmd,sp)

    # Continuously collect votlage and current data for 0.5 seconds
        t_readdata = time.time() + 10
        while time.time() < t_readdata:
            testfunctions.readVC(cmd, sp)

    # # Set constant current of 10A = 0x186A0 for 0.5 seconds
    #     cmd=[0]*26
    #     cmd[0]=0xAA
    #     cmd[2]=0x2A 
    #     cmd[3]=0xA0 # LSB of current value 10A = 100000*0.1mA = 0x186A0
    #     cmd[4]=0x86
    #     cmd[5]=0x01
    #     cmd[6]=0x00 # MSB
    #     cmd[25]=bk8500functions.csum(cmd)
    #     bk8500functions.cmd8500(cmd,sp)

        


# # Set constant current of 0A = 0x0
#     cmd=[0]*26
#     cmd[0]=0xAA
#     cmd[2]=0x2A 
#     cmd[3]=0x00 # LSB of current 
#     cmd[4]=0x00
#     cmd[5]=0x00
#     cmd[6]=0x00 # MSB
#     cmd[25]=bk8500functions.csum(cmd)
#     bk8500functions.cmd8500(cmd,sp)


# ### Turn OFF the load
#     cmd=[0]*26
#     cmd[0]=0xAA
#     cmd[2]=0x21
#     cmd[3]=0x00
#     cmd[25]=bk8500functions.csum(cmd)
#     bk8500functions.cmd8500(cmd, sp)

    resetload.resetLoad(cmd, sp)
    sp.close()

    
main()




