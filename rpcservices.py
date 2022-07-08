import servo_util
import xmlrpc.client
import json
PORTFORLOGGING=9501 # later we will make this an env variable. for now, use 9500-9550
PORTFORLEGS=9502 #position of each servo
PORTFORRAG=9503 #send rag commands here
PORTFORIMU=9504 #get 6dof (or better?) from here

logging = xmlrpc.client.ServerProxy('http://localhost:'+str(PORTFORLOGGING))

def log_start(command):
    logging.logstart(command)
def log_stop():
    logging.logstop()
def log_get():
    g=logging.logget()
    #print(g)
    return json.loads(g)
    
legs = xmlrpc.client.ServerProxy('http://localhost:'+str(PORTFORLEGS))

def leg_pos():
    return legs.legpos()

ragserver = xmlrpc.client.ServerProxy('http://localhost:'+str(PORTFORRAG))

def rag(name, reps=1,speedratio=1.0,modu=False,toldtowait=True):#dropping "savedata", as we have logger now
    return ragserver.rag(name,reps,speedratio,modu,toldtowait)

imuserver = xmlrpc.client.ServerProxy('http://localhost:'+str(PORTFORIMU))

def getimudata():#return pair of time and 7 element vector. later do better. some basic calibration (17 seconds)
    return imuserver.getimudata()

def getimupos():#return position, velocity and angle. calculated by basic integration. probably rather noisy and mistaken. but may be enough
    return imuserver.getimupos()

def imucalibn(n):#calibrate using n samples
    return imuserver.calibn(n)
    
def imuset(pos=False,vel=False,angle=False):#calibrate using n samples
    return imuserver.posset(pos,vel,angle)
