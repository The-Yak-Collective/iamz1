import sys
import os
import time
import threading
import ActionGroupControl as AGC
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ACTDIR=os.getenv('ACTDIR','/home/pi/SpiderPi/ActionGroups/')

print('''
run action groups by name
rag NAME TIMES
''')
args=sys.argv

if(len(args)==0):
    sys.exit("no action group specified")

f=os.listdir(ACTDIR)
actnames=[x[:-4] for x in f if x[-4:]=='.d6a']

times=1
if len(args)>1:
    times=int(args[2])
name=args[1]
if name in actnames:
    AGC.runActionGroup(name,times=times)
else:
    sys.exit("action not exist: "+ name+"see"+"\n".join(actnames))