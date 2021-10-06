import serial
import io

ser=serial.Serial('/dev/ttyUSB0', 115200,xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()
ser.flushOutput()
While True:
  data_raw = ser.read()
  print(data_raw.hex(), end=" ")