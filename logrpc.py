#service that logs start position and end position
import json
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import time
import servo_util
import csv
import threading

import os

import Mpu6050class as MPU
import Sonar as SONAR
import sys
import rpcservices
logfilename="/home/pi/test/iamz1/templogfile.csv" #decided to start with csv and go to sqlite obly if we need. for now we do not seem to (need to implement "log_get still")
from dotenv import load_dotenv, find_dotenv

mpu=None
sonar=None

PORTFORLOGGING=9501 #logging on/off port

LOGDIR=""

logstate=0 #0=not, 1=just started, 2=onging, 3=justended
incommand=""
thelock=threading.Lock()
eventdata=[]

def tick():
    global incommand,eventdata
    global thelock,logstate
    acquirepos=False
    eventname='event'+str(int(time.time()))
    with open(logfilename,"a") as f:
        writer=csv.writer(f)
        while True:
            if logstate==0:
                time.sleep(0.1)#we are asynchornous with events, lower accuracy, makes things more complex, but seems more correct for overall logging
                continue
            st=time.time()
            thelock.acquire()
            if logstate==1:
                eventdata=[] #new event so start collecting new set of event data
                eventname='event'+str(int(st))
                cmd=incommand
                acquirepos=True
                logstate=2
            elif logstate==2:
                acquirepos=False #maybe change this to simply lower frequency?
            elif logstate==3:
                acquirepos=True #we read pos at start and at end. and if we are fast enough, we do not do it twice. but we are never fast enough...
                logstate=0
            thelock.release()

            data=[]
            t=int(st*1000) #time in ms
            data.append(t)
            data.append(eventname)
            data.append(cmd)
            if acquirepos:
                poses=rpcservices.leg_pos()[1] #drop the initial timestamp
            else:
                poses=eventdata[-1][3:21]
            data=data+poses
            data=data+read6dof()
            data=data+readulsrangefinder()
            writer.writerow(data)
            f.flush()
            eventdata.append(data)
            t2=time.time()
            timelefttosleep=st+0.1-t2
            if timelefttosleep>0:
                time.sleep(timelefttosleep)#so we sample about each 0.1 seconds
                #print(timelefttosleep)
            else:
                print('(read is slow) timelefttosleep=',timelefttosleep, st,t2)

def main():
    global timestamp
    global LOGDIR

    global incommand,logfilename,logstate,eventdata
    
    #load_dotenv(find_dotenv())
    #LOGDIR=os.getenv('LOGDIR',"/home/pi/gdrive/logs/atestlog/")
    if not os.path.exists(logfilename):#consider LOGDIR+"datafile.csv"
        with open(logfilename,"a") as f:
            header=['time','eventid','cmd','p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12','p13','p14','p15','p16','p17','p16',"ax1","ay1","az1","gx1","gy1","gz1","temp","uls_range"]

            writer=csv.writer(f)
            writer.writerow(header)
            
    init6dof()
    inituls()

    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    # Create server
    with SimpleXMLRPCServer(('localhost', PORTFORLOGGING),
                            requestHandler=RequestHandler) as server:
        server.register_introspection_functions()


        # Register a function under a different name
        def logstart(command):
            global logstate,incommand, thelock,logfilename
            thelock.acquire()
            logstate=1
            incommand=command
            thelock.release()
            return logfilename #so you can read if you want
        def logstop():
            global logstate,incommand, thelock
            thelock.acquire()
            logstate=3
            thelock.release()
            return True

        def logget():
            global eventdata
            #readcsv=csv.reader(csvfile) #consider or simple store last "event"
            #print(eventdata)
            return json.dumps(eventdata) #[-1] #return last line logged - or maybe we can return it all!
        server.register_function(logstart, 'logstart')
        server.register_function(logstop, 'logstop')
        server.register_function(logget, 'logget')
        x=threading.Thread(target=tick, daemon=True)
        x.start()
        # Run the server's main loop
        server.serve_forever()

    
def read6dof():
    d=rpcservices.getimudata()
    res=d[1]
#    d=mpu.get_all_data()
#    res=[d[0]["x"],d[0]["y"],d[0]["z"],d[1]["x"],d[1]["y"],d[1]["z"],d[2]]
    return res

def readulsrangefinder():
    #return ("1975")
    global sonar
    #print("sonar", sonar.getDistance(), flush=True)
    return [sonar.getDistance()]
    

    
def init6dof():
    return # now handled by imurpc
    global mpu
    mpu = MPU.mpu6050(0x68)
    mpu.set_gyro_range(mpu.GYRO_RANGE_2000DEG)
    mpu.set_accel_range(mpu.ACCEL_RANGE_2G) 



def inituls():
    global sonar
    sonar=SONAR.Sonar()


main() #so i can play with function order