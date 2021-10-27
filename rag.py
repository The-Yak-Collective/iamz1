import sys
import os
import time
import threading
import ActionGroupControl as AGC
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ACTDIR=os.getenv('ACTDIR','/home/pi/SpiderPi/ActionGroups/')
import rpcservices

#print('''
#run action groups by name
#rag ACTIONFILENAME TIMES SPEEDRATIO MODU (true/falue) SAVEDATA (true/false)
#''')
args=sys.argv

if(len(args)<2): 
    sys.exit("no action group specified",str(args))
    
f=sorted(os.listdir(ACTDIR))
actnames=[x[:-4] for x in f if x[-4:]=='.d6a']
relactnames=[x[:-4] for x in f if x[-4:]=='.csv']

if(args[1]=="list"):
    print('list of available acts:\n')
    for x in actnames:
        print(x)
    for x in relactnames:
        print(x)
    sys.exit()

if(args[1]=="stop"):
    AGC.stopAction()
    sys.exit("stopped AG")
times=1
if len(args)>2:
    times=int(args[2])
    
speedratio=1.0
if len(args)>3:
    speedratio=float(args[3])
modu=False
if len(args)>4:
    modu=not (args[4] in ['false','False'])
savedata=False
if len(args)>5:
    savedata=not (args[5] in ['false','False'])
name=args[1]
if name.split('#')[0].split('@')[0] in actnames or name.split('#')[0].split('@')[0] in relactnames:
    rpcservices.log_start(name)
    print(AGC.runActionGroup(name,times=times, rs=speedratio, sd=savedata, modu=modu))
    rpcservices.log_stop()
else:
    sys.exit("action not exist: "+ name)