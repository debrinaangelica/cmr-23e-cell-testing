# DO WE WANT TO REST 100s AFTER DOING THE 0.5A - 15A SWITCH
# TODO: TEST IF FOR I IN RANGE ACTUALLY RUNS RANGE NUMBER OF TIMES
# TODO: TEST IF CURRENT LIMIT ACTUALLY LIMITS THE CURRENT
# TODO: FIND A WAY TO STORE DATA IN CSV FILE AND MARK TIMESTAMPS IN PARALLEL

# NOTE: STOP DISCHARGING WHEN CELL REACHES 2.8V

import signal
import serial
import time
import csv
import sys
import bk8500functions
import testfunctions
import resetload

### GLOBAL VARIABLES ###
datafile = 'testdata/test_cell_rest_4_15amp.csv'
# WARNING! 'w' will overwrite existing data
# use 'a' to add to existing data
CSVmode = 'a'  

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

sp.open()
print(sp)

def main():
    
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

# Set current limit to 20A
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x24
    cmd[3]=0x40 # LSB of current value 16A = 160000*0.1mA = 27100
    cmd[4]=0x0d
    cmd[5]=0x03
    cmd[6]=0x00 # MSB
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd,sp)

    # for i in range(num_test_cycles):
    while True:
    # Set constant current of 0.5A = 0x1388 for 10 seconds
        cmd=[0]*26
        cmd[0]=0xAA
        cmd[2]=0x2A
        cmd[3]=0x88 # LSB of current value 
        cmd[4]=0x13 # 88 13
        cmd[5]=0x00
        cmd[6]=0x00 # MSB
        cmd[25]=bk8500functions.csum(cmd)
        bk8500functions.cmd8500(cmd,sp)

        print("read data 0.5A:")
    # Continuously collect votlage and current data for 10 seconds
        t_readdata = time.time() + 10
        while time.time() < t_readdata:
        # for x in range(0, 75):
            testfunctions.readVC(cmd, sp)
            writer.writerow(get_load_data(cmd, sp))
            
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

        print("read data 15A:")
    # Continuously collect votlage and current data for 1 seconds
        t_readdata = time.time() + 2
        while time.time() < t_readdata:
        # for x in range (0, 15):
            testfunctions.readVC(cmd, sp)
            writer.writerow(get_load_data(cmd, sp))

# Set constant current of 0A = 0x0 
        resetload.resetLoad(cmd, sp)

        print("read data rest (0A):")
    # Rest the cell for 100s while reading current voltage data
        # t_readdata = time.time() + 30
        # while time.time() < t_readdata:
        # # for x in range (0, 800):
        #     # endTest = testfunctions.checkCutoffVoltage(cmd, sp)
        #     # if (endTest < 0):
        #     #     resetload.resetLoad(cmd, sp)
        #     #     sp.close()
        #     #     f.close()
        #     #     sys.exit()
        #     testfunctions.readVC(cmd, sp)
        #     writer.writerow(get_load_data(cmd, sp))
        time.sleep(20)

        main()


    # reset the load to 0A, 0V 
    resetload.resetLoad(cmd, sp)

    # close the serial port
    sp.close()
    
    # close the CSV file
    f.close()

    
main()




