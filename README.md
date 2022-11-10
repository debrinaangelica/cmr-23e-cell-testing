**How the electronic load works:**
We send instructions to it in the form of a 26-byte string of little-endian hex values.
No matter what instruction we send it, the load will respond with a 26-byte string. 
The first byte is always 0xaa. 

Main Test Script: test-rest.py

test-rest.py
Functions: Discharges at 0.5 A for 10 seconds, then discharges at 15 A for 2 seconds. Then turns the load off to rest the cell for 30 seconds. 
Issues: Unsure what the source is, but occasionally the data output by the electronic load is missing bytes 
Notes: Each time we write to the serial port, there is a delay of 0.2 seconds.
