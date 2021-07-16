#started (and killed) from iamz1 discord bot (using object.kill or .terminate)
#when run, create directory in gdrive/logs/NEWNAME
#set env to this dir value (or do we need to do all this in iamz1? probably, so also rag, etc. have it)
#functions: servors, including pos and temp (also volatge?)
#imu (6DOF)
#can we give camera pos?
#uls sensor
#snap image and save link (in sub folder called images and names as of time stamp

#also rag and cam create log files in same directory. csv. time, command, time of end, cam pos start and cam pos end (for cam)
#imports
import time
import Board
import os
import itertools
import Mpu6050class as MPU
import Sonar as SONAR
import cv2

from dotenv import load_dotenv, find_dotenv
mpu=None
sonar=None
cam=None
timestamp=0

def main():
    global timestamp
    load_dotenv(find_dotenv())
    USERHOMEDIR=os.getenv('USERHOMEDIR',"/media/pi/z1-drive/") 
    WHEREIRUNDIR=os.getenv('WHEREIRUNDIR',"/media/pi/z1-drive/maier/iamz1/") 
    LOGDIR=os.getenv('LOGDIR')
    os.mkdir(LOGDIR+"images/")

    #list of init functions
    inittime=lambda: ["time"]
    tmplabels=[["p"+str(x),"t"+str(x),"v"+str(x)] for x in range(1,19)] # could use itertools.Product
    initservo=lambda: [item for x in tmplabels for item in x] 

    init_funcs=[inittime,initservo,init6dof,inituls,initimage]
    #list of read functions
    read_funcs=[readtime,readservo,read6dof,readuls,readimage]
    readtime=lambda: int(time.time()*1000) #time in milliseconds


    #create datafile in that dir
    #run init functions and create list
    #csv-print list to file
    with open(LOGDIR+"datafile.csv",'a') as f:
        labels=[]
        for x in init_funcs:
            labels=labels+x()
        csvwrite(f,labels)
#create timestamp
#run read functions
#create output list
#write list to file+flush
        while True:
            data=[]
            timestamp=read_func[0]() #returns timestamp
            data[0]=timestamp
            for x in read_funcs[1:]:
                data=data+x()
            csvwrite(f,data)
#sleep what is left of a second
            nt=read_func[0]()-timestamp
            if(nt<1000):
                time.sleep((1000.0-nt)/1000.0)
            else:
                print("reading took over a second! {}".format(str(nt)))



def getBusServoStatus(ser):
    Pulse = Board.getBusServoPulse(ser)
    Temp = Board.getBusServoTemp(ser)
    Vin = Board.getBusServoVin(ser)
    return (Pulse,Temp,Vin)

def readservo():
    res=[]
    for x in range(1,19):
        p,t,v=getBusServoStatus(x)
        res=res +[str(p),str(t),str(v)]
    return res
    
def read6dof():
    d=mpu.get_all_data()
    res=[d[0]["x"],d[0]["y"],d[0]["z"],d[1]["x"],d[1]["y"],d[1]["z"],d[2]]
    
def readuls():
    global sonar
    return sonar.getDistance()
    
def readimage():
    global cam
    global timestamp
    img_name=str(timestamp)+".png"
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        cam = cv2.VideoCapture('/dev/video2')
        ret, frame = cam.read()

    if not ret:
        print("failed to grab frame")
    else:
        cv2.imwrite(LOGDIR+img_name, frame)
    cam.release()
    return(img_name)

    
def init6dof():
    global mpu
    mpu = MPU.mpu6050(0x68)
    mpu.set_gyro_range(mpu.GYRO_RANGE_2000DEG)
    mpu.set_accel_range(mpu.ACCEL_RANGE_2G) 
    return ["ax1","ay1","az1","gx1","gy1","gz1","temp"]

def initimage():

    return ["imagefile"]

def inituls():
    global sonar
    sonar=SONAR.Sonar()
    return ["uls range"]

def csvwrite(f,data):
    for x in data[:-1]
        f.write('"'+str(x)+'",')
    f.write('"'+str(x)+'"')
    f.flush()
    
main() #so i can play with function order