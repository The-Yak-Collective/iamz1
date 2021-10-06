#seems to read ok
#now put in all the commands and show one command per line in plain english, based on protocol standard

import serial
import io
import time

HEADER         = 0x55

coms=[["MOVE_TIME_WRITE",1,7],
["MOVE_TIME_READ",2,3,7],
["MOVE_TIME_WAIT_WRITE",7,7],
["MOVE_TIME_WAIT_READ",8,3,7],
["MOVE_START",11,3],
["MOVE_STOP",12,3],
["ID_WRITE",13,4],
["ID_READ",14,3,4],
["ANGLE_OFFSET_ADJUST",17,4],
["ANGLE_OFFSET_WRITE",18,3],
["ANGLE_OFFSET_READ",19,3],
["ANGLE_LIMIT_WRITE",20,7],
["ANGLE_LIMIT_READ",21,3,7],
["VIN_LIMIT_WRITE",22,7],
["VIN_LIMIT_READ",23,3,7],
["TEMP_MAX_LIMIT_WRITE",24,4],
["TEMP_MAX_LIMIT_READ",25,3,4],
["TEMP_READ",26,3,4],
["VIN_READ",27,3,5],
["POS_READ",28,3,5],
["OR_MOTOR_MODE_WRITE",29,7],
["OR_MOTOR_MODE_READ",30,3,7],
["LOAD_OR_UNLOAD_WRITE",31,4],
["LOAD_OR_UNLOAD_READ",32,3,4],
["LED_CTRL_WRITE",33,4],
["LED_CTRL_READ",34,3,4],
["LED_ERROR_WRITE",35,4],
["LED_ERROR_READ",36,3,4]]


def checksum(buf):
    sum = 0x00
    for b in buf:  # 求和
        sum += b
    sum = sum 
    sum = ~sum  # 取反
    return sum & 0xff

ser=serial.Serial('/dev/ttyUSB0', 115200,xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()



while True:
    for c in ser.read():
        if int(c) == 0x55:
            #print("0x55_1 ",end=" ")
            c=ser.read()
            if ord(c) == 0x55: #so we have two in a row
                #print("0x55_2 ",end=" ")
                #readitem=bytearray(0)
                payload=bytearray(0)
                id=ser.read()
                #print(type(readitem),type(id))
                length=ser.read()
                readitem=bytearray(ord(length))
                cmd=ser.read()
                if ord(length)>3:
                    #print(length, ord(length))
                    payload=bytearray(ser.read(ord(length)-3))
                    #print("payload:",payload.hex(),len(payload))
                chksum=ser.read()
                #print(type(readitem),type(id),type(payload))
                readitem[0]=ord(id)
                readitem[1]=ord(length)
                readitem[2]=ord(cmd)
                for i in range(3,len(payload)+3):
                    readitem[i]=payload[i-3]
                #print(readitem, readitem.hex(), ord(chksum), checksum(readitem), end=" ")
                if ord(chksum) != checksum(readitem):
                    print("checksum fail!",readitem,"read=",ord(chksum), "calc=",checksum(readitem))
                    continue
                line=[x for x in coms if x[1]==ord(cmd)]
                #print("line=",line)
                if len(line)==0:
                    print("illegal command")
                    continue
                line=line[0]
                if ord(length)==line[2]:
                    print("write", end=" ")
                elif len(line)>3 and ord(length)==line[3]:
                    print("read", end=" ")
                print(line[0], "servo=", ord(id),  end=" ") #ord(length), ord(cmd),payload, - if we want to see raw form
                if ord(length)==7:
                    print(int.from_bytes(payload[0:2],'little'), end=" ")
                    print(int.from_bytes(payload[2:4],'little'))
                elif ord(length)==4:
                    print(payload[0])
                elif ord(length)==5:
                    print(int.from_bytes(payload[0:2],'little'))
                else:
                    print(" ")
                break #finished a command unit, i hope
            else:
                print("half a header: ",c.hex())
        else:
            print("skipping: ",hex(c))