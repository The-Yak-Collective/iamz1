#service that returns current gyro, acc, temp and also does integration and keeps a position log, so you can compare. or maybe only recalls compared to 0 time.
#for now, use very low quality pos estimation
import json
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import time
import servo_util
import csv
import threading

import os

import Mpu6050class as MPU
import sys
import rpcservices

from dotenv import load_dotenv, find_dotenv

mpu=None

RES6DOF = 0.1 #accuracy of raw data = every 100 ms. play with it...
PORTFORIMU=9504 #IMU data port
calib=[0,0,0,0,0,0,0]
pos=[0,0,0]
angle=[0,0,0]
lastrecorded=(0,[]) #change a bit as we need to have continuous
rawdata=[] #need some way to limit this to say last 1000 datums, etc
TOOBIG=10000
ENOUGH=1000
def tick():
    global rawdata, calib, pos, angle #not really raw any more data as we calibrate it...
    while True:
        st=time.time()
        t=int(st*1000) #time in ms
        eventdata=read6dof()
        for i in range(len(eventdata)):
            eventdata[i]=eventdata[i]-calib[i]
        rawdata.append((st,eventdata)) #t is simply too large for xml int
        if len(rawdata)>TOOBIG:
            del rawdata[TOOBIG-ENOUGH:]
        #and now (not yet here) calculate pos and angle
        t2=time.time()
        timelefttosleep=st+0.1-t2
        if timelefttosleep>0:
            time.sleep(timelefttosleep)#so we sample about each 0.1 seconds
            #print(timelefttosleep)
        else:
            print('(read is slow) timelefttosleep=',timelefttosleep, st,t2)

def main():
    global timestamp

    init6dof()

    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    # Create server
    with SimpleXMLRPCServer(('localhost', PORTFORIMU),
                            requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        # Register a function under a different name
        def getimudata(): #no locking, for now, but probably should have...
            global lastrecorded,rawdata
#            t=time.time()
#            if t-lastrecorded[0]>RES6DOF:
#                lastrecorded=(t,read6dof())
#            return (lastrecorded,rawdata[-1]) #needs work - as should only return the data from raw data
            try:
                print(rawdata[-1],len(rawdata))
                return (rawdata[-1]) #needs work - as should only return the data from raw data
            except:
                return(0,[0,0,0,0,0,0,0])

        server.register_function(getimudata, 'getimudata')
        x=threading.Thread(target=tick, daemon=True) #when tick works, will open this and then getimudata should be pure "read form the stack"
        x.start()
        # Run the server's main loop
        server.serve_forever()

    
def read6dof():
    d=mpu.get_all_data()
    res=[d[0]["x"],d[0]["y"],d[0]["z"],d[1]["x"],d[1]["y"],d[1]["z"],d[2]]
    return res

    
def init6dof():
    global mpu
    global calib
    t1=time.time()
    data=[]
    mpu = MPU.mpu6050(0x68)
    mpu.set_gyro_range(mpu.GYRO_RANGE_2000DEG)
    mpu.set_accel_range(mpu.ACCEL_RANGE_2G)
    for i in range(100):
        readit=read6dof()
        data.append(readit) #100 readings. now lets average them
        for i in range(len(readit)):
            calib[i]=calib[i]+readit[i]
    for i in range(len(calib)):
        calib[i]=claib[i]/100
    t2=time.time()
    print(calib, t2-t1) #for now, we are also zeroing the z axis. oh well...
    



main() #so i can play with function order