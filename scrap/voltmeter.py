# 
import sys, dcload
from time import time
from win32com.client import Dispatch
from msvcrt import kbhit

# change port and baudrate to  match the port and 
# baudrate settings used to interface on the PC.
port = 5
baudrate = 38400


load = Dispatch('BKServers.DCLoad85xx')
load.Initialize(port, baudrate) # Open a serial connection
load.SetRemoteControl()
of = open("fast.dat", "w")
start = time()
count = 1
while True:
    msg = "%6d %8.2f s %s\n" % (count, time() - start, load.GetInputValues())
    of.write(msg)
    if kbhit():
        break
    count += 1
finish = time() - start
load.SetLocalControl()
of.write("\nReading rate = %.1f readings/second\n" % (count/finish))
print "\n Reading rate = %.1f readings/second\n" % (count/finish)
