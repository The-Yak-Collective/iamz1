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
        print(data_raw.hex(), end=" ")
    else:
        time.sleep(0.01)