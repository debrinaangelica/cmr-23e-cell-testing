# Data file:
#  Header info:
#  # Command line
#  # Date and time for start of test
#  Entry info:
#  time voltage current power
#  time is in seconds since start of test
#  Other measurements are in V, A, and W
# We talk to a DC load using COM.

import sys #, dcload
# from win32com.client import Dispatch
# from string import join
from time import time, sleep
from msvcrt import kbhit, getch
out = sys.stdout.write
nl = "\n"
interval_s = 1 # Interval between readings

def Usage():
    name = sys.argv[0]
    msg = "input: filenameForData"
    locals()
    print(msg) # set in line 22
    exit(1)

def ProcessCommandLine():
    if len(sys.argv) < 6:
        Usage()
    port = 'COM6'
    mode = 'cc' #constant current
    value = 20 # 20A
    cov = 0 # cut-off voltage (what's this?)
    filename = sys.argv[1] + ".dat"
    docstring = ""
    if len(sys.argv) > 6:
        docstring = join(sys.argv[6:])
        # Check values
        assert(port >= 0)
        assert(mode in ("cc", "cv", "cp", "cr"))
        assert(value > 0)
        assert(cov > 0)
        from os.path import exists
        assert(not exists(filename))
        out("Mode = %s\n" % mode)
        out("Value = %s\n" % value)
        out("cov = %s\n" % cov)
        out("filename = %s\n" % filename)
        return port, mode, value, cov, filename, docstring

def Set(task, error_message):
    if error_message:
        out("Error on task '%s':\n" % task)
        out(error_message)
        exit(1)

def SetModeAndValue(load, mode, value):
    # Set mode and value. Also check that the maximum setting is at
    # least the value we want.
    Set("Set to mode %s" % mode, load.SetMode(mode))
    if mode == "cc":
        max_current = float(load.GetMaxCurrent())
        if max_current < value:
            out("Max current setting is less than desired value" + nl)
            exit(1)
        Set("Set to value %g" % value, load.SetCCCurrent(value))
    elif mode == "cv":
        max_voltage = float(load.GetMaxVoltage())
        if max_voltage < value:
            out("Max voltage setting is less than desired value" + nl)
            exit(1)
        Set("Set to value %g" % value, load.SetCVVoltage(value))
    elif mode == "cp":
        max_power = float(load.GetMaxPower())
        if max_power < value:
            out("Max power setting is less than desired value" + nl)
            exit(1)
        Set("Set to value %g" % value, load.SetCWPower(value))
    else:
        Set("Set to value %g" % value, load.SetCRResistance(value))

def GetCurrentVoltagePower(load):
    def get_value(f):
        value, unit = f.split()
        return float(value)
    s = load.GetInputValues()
    fields = s.split("\t")
    voltage = get_value(fields[0])
    current = get_value(fields[1])
    power = get_value(fields[2])
    return voltage, current, power

def RunTest(log, load, mode, value, cov):
    def LogMsg(msg):
        out(msg)
        log(msg)
    load.SetRemoteControl()
    SetModeAndValue(load, mode, value)
    log("# Command line: %s\n" % join(sys.argv[1:]))
    'log("# %s\n" % version)'
    msg = "# Test start time = " + load.TimeNow() + nl
    LogMsg(msg)
    Set("Turn load on", load.TurnLoadOn())
    voltage, current, power = GetCurrentVoltagePower(load)
    start_time = time()
    while voltage >= cov:
        voltage, current, power = GetCurrentVoltagePower(load)
        current_time = time() - start_time
        LogMsg("%9.2f %9.4f %8.4f %9.4f\n" % \
            (current_time, voltage, current, power))
        sleep(interval_s)
        if kbhit():
            c = getch()
            if c == "Q":
                break
    Set("Turn load off", load.TurnLoadOff())
    LogMsg("# Test finish time = " + load.TimeNow() + nl)
    load.SetLocalControl()

def main():
    port, mode, value, cov, filename, docstring = ProcessCommandLine()
    load = Dispatch('BKServers.DCLoad85xx')
    baudrate = 9600
    load.Initialize(port, baudrate) # Open a serial connection
    log = open(filename, "w").write
    RunTest(log, load, mode, value, cov)

main()