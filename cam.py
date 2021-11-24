import sys
import os
import time
import Board
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

args=sys.argv
PAN=2
TILT=1
STEP=100 # size of +/- steps
SPEEDTIME=500 #milliseconds to move in 

if(len(args)<2): 
    sys.exit("no cam action specified. try 'list'",str(args))
try:
    readpos()
except:
    pass

def savepos():
    with open('campos.txt','w') as f:
        f.write('{0}\n{1}\n'.format(str(Board.Servos[PAN-1].getPosition()),str(Board.Servos[TILT-1].getPosition())))
    #print('saved:',str(Board.Servos[PAN-1].getPosition()),str(Board.Servos[TILT-1].getPosition()))
    
def readpos():
    with open('campos.txt','r') as f:
        g=f.readlines()
        #print('got ',int(g[0]),int(g[1]))
    Board.Servos[PAN-1].Position=int(g[0])
    Board.Servos[TILT-1].Position=int(g[1])
    #print('set', Board.Servos[PAN-1].Position,Board.Servos[TILT-1].Position)

readpos()
    
def pos():
    #print(TILT-1,PAN-1,Board.Servos[0].Position,Board.Servos[1].Position)
    return Board.Servos[TILT-1].getPosition(),Board.Servos[PAN-1].getPosition()
    
def setpos(id,x):
    if x<500:
        x=500
    if x>2500:
        x=2500
    #print('setting servo {} to {} with speed {}'.format(id,x,SPEEDTIME))
    Board.setPWMServoPulse(int(id),int(x),int(SPEEDTIME))
    time.sleep(SPEEDTIME/1000.0)
    savepos()
    return
   


if(args[1]=="list"):
    print('''list of available cam commands:
    pan go  => slow move from left to right end where was
    tilt go => slow move top down end where was
    pan X => pan to positon X range {500..2500}
    tilt X => tilt to positon X range {500..2500}
    pan + => add 100 to pan position
    pan - => subtract 100 from pan position
    tilt + => add 100 to tilt position
    tilt - => subtract 100 from tilt position
    X Y => goto position X,Y
    pos => show pos
    rest => goto 1500,1500 - center position
    list => this list
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
sid=PAN #not needed, but lets see
if (args[1]=='pan'):
    sid=PAN
elif (args[1]=='tilt'):
    sid=TILT
else:
    sys.exit('illegal command')
if len(args)<3:
    sys.exit('need at least one argument after pan/tilt')
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

