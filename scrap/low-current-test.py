# DO WE WANT TO REST 100s AFTER DOING THE 0.5A - 15A SWITCH
# TODO: TEST IF FOR I IN RANGE ACTUALLY RUNS RANGE NUMBER OF TIMES
# TODO: TEST IF CURRENT LIMIT ACTUALLY LIMITS THE CURRENT
# TODO: FIND A WAY TO STORE DATA IN CSV FILE AND MARK TIMESTAMPS IN PARALLEL

# REFERENCE: List of currents in hex
# 3A    = 0x7530
# 0.5A  = 0x1388
# 1A    = 0x2710
# 10A   = 0x186A0
# 15A   = 0x249F0
# 20A   = 

import signal
import serial
import time
import csv
import sys
import bk8500functions
import testfunctions
import resetload

### GLOBAL VARIABLES ###
datafile = 'testdata/test_cell_2.csv'
# WARNING! 'w' will overwrite existing data
# use 'a' to add to existing data
CSVmode = 'w'  

length_packet = 26
num_test_cycles = 10
sp = serial.Serial()
sp.setBaudrate = 9600
sp.port = 'COM6'
cmd=[0]*26
### END OF GLOBAL VARIABLES ###

# INITIALIZE CSV FILE
# open the file in the write mode
f = open(datafile, CSVmode,  newline='')
# create the csv writer
writer = csv.writer(f)
# write the header for the data
fieldnames = ['timestamp', 'voltage', 'current']
if (CSVmode == 'w'):
    writer.writerow(fieldnames)

# ctrl-C to abort if something goes wrong
def abort(signum, frame):
    resetload.resetLoad(cmd, sp)
    sys.terminate()

# returns the load data as an array to store in csv file
# format [timestamp, voltage, current]
def get_load_data(cmd, sp):
    load_data = []
    load_data.append(time.time())
    load_data.extend(testfunctions.readVC(cmd, sp))
    return load_data

def main():
    sp.open()
    print(sp)
    signal.signal(signal.SIGINT, abort) 
    
## Set to remote command
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

# Set current limit to !20A!
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x24
    cmd[3]=0x40 # LSB of current value 20A = 0x30d40
    cmd[4]=0x0d
    cmd[5]=0x03
    cmd[6]=0x00 # MSB
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd,sp)

# Set constant current of 0.5A for 10 seconds
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x2A
    cmd[3]=0x88 # LSB of current value 
    cmd[4]=0x13 # note: cannot write a current higher 
    cmd[5]=0x00       # than the limit without error
    cmd[6]=0x00 # MSB
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd,sp)

    print("read data 0.5A:")
    for x in range(0,5):
        testfunctions.readVC(cmd, sp)
        writer.writerow(get_load_data(cmd, sp))


# Set constant current of 1A for 10 seconds
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x2A
    cmd[3]=0x10 # LSB of current value 
    cmd[4]=0x27 # note: cannot write a current higher 
    cmd[5]=0x00       # than the limit without error
    cmd[6]=0x00 # MSB
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd,sp)

    print("read data 1A:")
    for x in range(0,5):
        testfunctions.readVC(cmd, sp)
        writer.writerow(get_load_data(cmd, sp))

# Set constant current of 1.5A for 10 seconds
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x2A
    cmd[3]=0x98 # LSB of current value 
    cmd[4]=0x3a # note: cannot write a current higher 
    cmd[5]=0x00       # than the limit without error
    cmd[6]=0x00 # MSB
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd,sp)

    print("read data 1.5A:")
    for x in range(0,5):
        testfunctions.readVC(cmd, sp)
        writer.writerow(get_load_data(cmd, sp))


    resetload.resetLoad(cmd, sp)
    sp.close()
    
    # close the CSV file
    f.close()

    
main()




