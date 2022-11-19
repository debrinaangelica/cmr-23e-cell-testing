import bk8500functions

def DecodeInteger(self, str):
    # '''Construct an integer from the little endian string. 1, 2, and 4 byte 
    # strings are the only ones allowed.
    # '''
    assert(len(str) == 1 or len(str) == 2 or len(str) == 4)
    n  = ord(str[0])
    if len(str) >= 2:
        n += (ord(str[1]) << 8)
        if len(str) == 4:
            n += (ord(str[2]) << 16)
            n += (ord(str[3]) << 24)
    return n

def GetInputValues(cmd, ser):
    # '''Returns voltage in V, current in A, and power in W, op_state byte,
    # and demand_state byte.
    # '''
    #Set voltage limit
    cmd=[0]*26
    cmd[0]=0xAA
    cmd[2]=0x22
    cmd[3]=0x66
    cmd[4]=0x3f
    cmd[25]=bk8500functions.csum(cmd)
    bk8500functions.cmd8500(cmd,ser)


    voltage = self.DecodeInteger(response[3:7])/self.convert_voltage
    current = self.DecodeInteger(response[7:11])/self.convert_current
    power   = self.DecodeInteger(response[11:15])/self.convert_power
    op_state = hex(self.DecodeInteger(response[15]))
    demand_state = hex(self.DecodeInteger(response[16:18]))
    s = [str(voltage) + " V", str(current) + " A", str(power) + " W", str(op_state), str(demand_state)]
    return join(s, "\t")