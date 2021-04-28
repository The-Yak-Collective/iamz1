import sys
import os
import time
import threading
import ActionGroupControl as AGC
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ACTDIR=os.getenv('ACTDIR','/home/pi/SpiderPi/ActionGroups/')


f=os.listdir(ACTDIR)
actnames=[x[:-4] for x in f if x[-4:]=='.d6a']

for x in actnames:
    print(x)
