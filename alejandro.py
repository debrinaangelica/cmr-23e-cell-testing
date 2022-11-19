def CommandProperlyFormed(self, cmd):
    # Return 1 if command is properly formed
    # zero if not proper

    # Proper length
    if len(cmd) != self.length_packet:
        print("Command BAD")
        return 0

    # First character must be 0xaa
    if ord(cmd[0]) != 0xaa:
        print("First byte is not 0xaa!")
        return 0

    # Second character must not be 0xff
    if ord(cmd[0]) == 0xff:
        print("Second byte should not be 0xff!")
        return 0

    # Calculate checksum and validate
    checksum = self.CalculateChecksum(cmd)
    if checksum != ord(cmd[-1]):
        print("Wrong checksum!")
        return 0

    # all requirements passed
    return 1

def CalculateChekcsum(self, cmd):
    assert((len(cmd) == self.length_packet - 1) or (len(cmd) == self.length_packet))
    checksum = 0
    for i in range(self.length_packet - 1):
        checksum += ord(cmd[i])
        checksum %= 256
        return checksum

def StartCommand(self, byte):
    return chr(0xaa) + chr(self.address) + chr(byte)

def SendCommand(self, command):
    # sends the command to the serial stream and returns the 26 bytes response
    assert(len(command) == self.length_packet)
    self.sp.write(command)
    response = self.sp.read(self.length_packet)
    assert(len(command) == self.length_packet)
    return response

def ResponseStatus(self, response):
    # Return a message string about what the resmonse meant. 
    # Empty string means response is OK
    responses = {
        0x90 : "Wrong checksum",
        0xA0 : "Incorrect parameter value",
        0xB0 : "Command cannot be carried out",
        0xC0 : "Invalid command",
        0x80 : "",
    }
    assert(len(response) == self.length_packet)
    assert(ord(response[2]) == 0x12)
    return responses[ord(response[3])]


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

def GetInputValues(self):
    # '''Returns voltage in V, current in A, and power in W, op_state byte,
    # and demand_state byte.
    # '''
    cmd = self.StartCommand(0x5F)
    cmd += self.Reserved(3)
    cmd += chr(self.CalculateChecksum(cmd))
    assert(self.CommandProperlyFormed(cmd))
    response = self.SendCommand(cmd)
    self.PrintCommandAndResponse(cmd, response, "Get input values")
    voltage = self.DecodeInteger(response[3:7])/self.convert_voltage
    current = self.DecodeInteger(response[7:11])/self.convert_current
    power   = self.DecodeInteger(response[11:15])/self.convert_power
    op_state = hex(self.DecodeInteger(response[15]))
    demand_state = hex(self.DecodeInteger(response[16:18]))
    s = [str(voltage) + " V", str(current) + " A", str(power) + " W", str(op_state), str(demand_state)]
    return join(s, "\t")