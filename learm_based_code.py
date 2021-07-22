#!/usr/bin/env python
from time import sleep
import serial
import binascii
from multiprocessing import Process, Queue

FRAME_HEADER = 0x55
CMD_SERVO_MOVE = 0x03
CMD_ACTION_GROUP_RUN = 0x06
CMD_ACTION_GROUP_STOP = 0x07
CMD_ACTION_GROUP_SPEED = 0x0B
CMD_GET_POSITIONS = 0x15
CMD_GET_BATTERY_VOLTAGE = 0x0F

BATTERY_VOLTAGE = 0x0F
ACTION_GROUP_RUNNING = 0x06
ACTION_GROUP_STOPPED = 0x07
ACTION_GROUP_COMPLETE = 0x08

#maximum and minimum positions each servo can travel
clawLimits = [200,700] #ID1
wristRotLimits = [0,1000] #ID2
wristLimits = [0,1000] #ID3
elbowLimits = [0,700] #ID4
shoulderLimits = [150,800] #ID5
rotationLimits = [0,1000] #ID6

#Serial Queues for reading and writing
rQueue = Queue()
wQueue = Queue()

#converts -135/135 (servo range +/- 30) to 0-1000 (servo position unit)
def anglesToPositions(angles):
	positions = []
	for angle in angles:
		positions.append(int(round((angle+135)/270 * 1000)))
	return positions

#converts 0-1000 (servo position unit as integer) to -135/135 (servo range +/- 30 as float)
def positionsToAngles(positions):
	angles = []
	for pos in positions:
		angles.append((pos/1000 * 270)-135)
	return angles

#private worker method for startSerialProcess()
def openSerialPort(writeQueue,readQueue):
	serialData = serial.Serial(
		port='/dev/ttyAMA1', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0 - i followed https://www.raspberrypi.org/forums/viewtopic.php?t=244528 for uart5 that maps to pins 14 and 15. i tried with flow control (in /boot/config.txt). could be that the AMA# depends on how many uarts you enabled. /dev/tty* shows AMA0 and AMA1. before there was? do without flow control. teh whole uart thing is complicated with all teh pin, gpio etc numbers. see https://www.raspberrypi.org/documentation/configuration/uart.md possibly it shoudl simply be AMA0. lets see. no. AMA0 is the servos bus and set at 115k baud
		baudrate = 9600,
		bytesize=serial.EIGHTBITS,
		timeout=None
		)
	#serialData.flushInput()
	#serialData.flushOutput()
	try:
		while True:
			if(serialData.inWaiting()):
				byte = serialData.read(1)
				readQueue.put(byte)
			if(not writeQueue.empty()):
				byte = writeQueue.get()
				serialData.write(byte)
	finally:
		serialData.close()

#Call to begin listining to the serial port. Uses openSerialPort
def startSerialProcess():
	p = Process(target=openSerialPort, args=(wQueue,rQueue))
	p.daemon = True
	p.start()

#Move all servo/angle combos in the time provided
#Ordered by servo ID NOT by J axis
def moveServos(servoIDs, positions, time):
	numOfServos = len(servoIDs)
	#check if each servo has a corresponding time and angle
	if (len(positions) != numOfServos):
		print("Provided positions or times do not match the number of servos requested. Exiting...")
		return
	#print("Moving Servos: " + str(servoIDs))

	packetLength = 5 + 3*numOfServos
	#create packet header
	cmdbytes = bytearray(4)
	cmdbytes[0] = FRAME_HEADER  #header 1
	cmdbytes[1] = FRAME_HEADER  #header 2
	cmdbytes[2] =  packetLength #packet length
	cmdbytes[3] = CMD_SERVO_MOVE  #command number
	cmdbytes.append(numOfServos) #number of servos that will move
	timeLSB = time & 0xFF #least significant bit
	timeMSB = (time >> 8) & 0xFF #most significant bit
	cmdbytes.append(timeLSB)
	cmdbytes.append(timeMSB)

	for i in range(numOfServos):
		#split angle into 2 bytes
		posLSB = positions[i] & 0xFF
		posMSB = (positions[i] >> 8) & 0xFF
		#per servo parameters
		cmdbytes.append(servoIDs[i])
		cmdbytes.append(posLSB)
		cmdbytes.append(posMSB)

	#bytesAsHex = ' '.join(format(x, '02x') for x in cmdbytes)
	#print(bytesAsHex)
	wQueue.put(cmdbytes)
	sleep(time/1000)

#Stop all servos, 1-6
def powerOffServos():
	wQueue.put(bytearray.fromhex("5555091406010203040506"))

#Saved in robot memory
def runActionGroup(groupNumber,iterations=1):
	#create packet header
	cmdbytes = bytearray(7)
	cmdbytes[0] = FRAME_HEADER  #header 1
	cmdbytes[1] = FRAME_HEADER  #header 2
	cmdbytes[2] = 0x05 #packet length
	cmdbytes[3] = CMD_ACTION_GROUP_RUN  #command number
	cmdbytes[4] = groupNumber

	itrLSB = iterations & 0xFF #least significant bit
	itrMSB = (iterations >> 8) & 0xFF #most significant bit
	cmdbytes[5] = itrLSB
	cmdbytes[6] = itrMSB

	bytesAsHex = ' '.join(format(x, '02x') for x in cmdbytes)
	#print(bytesAsHex)
	wQueue.put(cmdbytes)

#Cancel running action group
def stopActionGroup():
	#create packet header
	cmdbytes = bytearray(4)
	cmdbytes[0] = FRAME_HEADER  #header 1
	cmdbytes[1] = FRAME_HEADER  #header 2
	cmdbytes[2] = 0x02 #packet length
	cmdbytes[3] = CMD_ACTION_GROUP_STOP  #command number
	bytesAsHex = ' '.join(format(x, '02x') for x in cmdbytes)
	#print(bytesAsHex)
	wQueue.put(cmdbytes)

#get current servo positions
def readPositions():
	#create packet header
	cmdbytes = bytearray(11)
	cmdbytes[0] = FRAME_HEADER  #header 1
	cmdbytes[1] = FRAME_HEADER  #header 2
	cmdbytes[2] = 0x09 #packet length
	cmdbytes[3] = CMD_GET_POSITIONS  #command number
	cmdbytes[4] = 0x06
	cmdbytes[5] = 0x01
	cmdbytes[6] = 0x02
	cmdbytes[7] = 0x03
	cmdbytes[8] = 0x04
	cmdbytes[9] = 0x05
	cmdbytes[10] = 0x06
	bytesAsHex = ' '.join(format(x, '02x') for x in cmdbytes)
	#print(bytesAsHex)
	wQueue.put(cmdbytes)

#######
# Predefined Positional Commands
#######

#Move all servos to home position
def homeServos():
	moveServos([1,2,3,4,5,6], [200,127,791,207,656,508], 3000)

def closeClawMax():
	moveServos([1], [clawLimits[0]], 500)
	
def closeClawKeg():
	moveServos([1], [390], 500)

def openClaw():
	moveServos([1], [clawLimits[1]], 500)

class ServoComms:
	def __init__(self):
		startSerialProcess()
		# ~ sleep(5)
		# ~ moveServos([4,6], [300,400], 1000)
		# ~ sleep(3)
		#homeServos()
		#readPositions()
		#runActionGroup(7,2)
		#sleep(3)
		# ~ stopActionGroup()


		# ~ while True:
			# ~ if(not rQueue.empty()):
				# ~ byte = rQueue.get()
				# ~ print(binascii.hexlify(byte))