# Main Test Script: test-rest.py

## About the Electronic Load

**How the electronic load works:**

We send instructions to it in the form of a 26-byte string of little-endian hex values.
No matter what instruction we send it, the load will respond with a 26-byte string. 
The first byte is always 0xaa. 

## Test Scripts

### test-rest.py

**What does this script do:**

Discharges at 0.5 A for 10 seconds, then discharges at 15 A for 2 seconds. Then turns the load off to rest the cell for 30 seconds. 

**Issues**: Unsure what the source is, but occasionally the data output by the electronic load is missing bytes, or the bytes are not output in the correct order. 

**Notes**: Each time we write to the serial port, there is a delay of 0.2 seconds.

## CSV files

[9/11/22] **test_cell_rest__15amp.csv**: Data from cell discharge test using the test-rest.py script.
- Some of the data (relatively minor amount) is inaccurate due to the issues related to the output of the load. 

## Useful Sources

[BK85xx Programming Manual](https://bkpmedia.s3.amazonaws.com/downloads/manuals/en-us/85xx_manual.pdf) 

[Sample test scripts from the manufacturer](https://github.com/BKPrecisionCorp/BK-8500-Electronic-Load)
