import sys
import os
import time
import Board
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ACTDIR=os.getenv('ACTDIR','/home/pi/SpiderPi/ActionGroups/')


args=sys.argv
PAN=2
TILT=1
STEP=100 # size of +/- steps
SPEEDTIME=500 #milliseconds to move in 
if(len(args)<2): 
    sys.exit("no cam action specified. try 'list'",str(args))

def pos():
    return Board.Servos[TILT-1].getPosition(),Board.Servos[PAN-1].getPosition()
def setpos(id,x):
    return Board.setPWMServoPulse(id,x,SPEEDTIME)

if(args[1]=="list"):
    print('''list of available cam commands:
    pan go slow move from left to right end where was
    tilt go slow move top down end where was
    pan X pan to positon X range {500..2500}
    tilt X tilt to positon X range {500..2500}
    pan + add 100 to pan position
    pan - subtract 100 from pan position
    tilt + add 100 to tilt position
    tilt - subtract 100 from tilt position
    X Y  goto position X,Y
    pos  show pos
    rest  goto 1500,1500 - center position
    list this list
    ''')
    sys.exit(pos())

if (args[1]=='pos'):
    sys.exit(pos())
if (args[1]=='rest'):
    setpos(PAN,1500)
    setpos(TILT,1500)
    sys.exit(pos())
if (args[1].isdigit() and args[2].isdigit()):
    setpos(PAN,int(args[1]))
    setpos(TILT,int(args[2]))
    sys.exit(pos())
if (args[1]=='pan'):
    sid=PAN
if (args[1]=='TILT'):
    sid=TILT
#from here, only second arg matters
if (args[2].isdigit()):
    setpos(sid,int(args[2]))
    sys.exit(pos())
if (args[2]=='-'):
    temp=pos()[sid-1]
    setpos(sid,temp-STEP)
    sys.exit(pos())
if (args[2]=='+'):
    temp=pos()[sid-1]
    setpos(sid,temp+STEP)
    sys.exit(pos())
if (args[2]=='go'):
    temp=pos()[sid-1]
    setpos(sid,500)
    for x in range (500+STEP,2500+STEP,STEP):
        setpos(sid,x)
    setpos(sid,temp)
    sys.exit(pos())
