#seems to read ok
#now put in all the commands and show one command per line in plain english, based on protocol standard

import serial
import io
import time

ser=serial.Serial('/dev/ttyUSB0', 115200,xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()
ser.flushOutput()
while True:
    bytesToRead = ser.inWaiting()
    if bytesToRead >0:
        data_raw = ser.read(bytesToRead)
        print(data_raw.hex())
    else:
        time.sleep(0.01)