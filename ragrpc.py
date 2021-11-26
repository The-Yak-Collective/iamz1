from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import time
import servo_util
import sys
import os
import time
import threading
import ActionGroupControl as AGC
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ACTDIR=os.getenv('ACTDIR','/home/pi/SpiderPi/ActionGroups/')
import rpcservices
import json

PORTFORRAG=9503 #position of each servo

f=sorted(os.listdir(ACTDIR))
actnames=[x[:-4] for x in f if x[-4:]=='.d6a']
relactnames=[x[:-4] for x in f if x[-4:]=='.csv']


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server
with SimpleXMLRPCServer(('localhost', PORTFORRAG),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()


    # Register a function under a different name
    def rag(name, times, speedratio,modu,toldtowait):
        if(name=="list"): #list rebuilds list as well!
            global actnames,relactnames
            f=sorted(os.listdir(ACTDIR))
            actnames=[x[:-4] for x in f if x[-4:]=='.d6a']
            relactnames=[x[:-4] for x in f if x[-4:]=='.csv']

            return actnames+relactnames

        if(name=="stop"):
            AGC.stopAction()
            return("stopped AG")

        if name.split('#')[0].split('@')[0] in actnames or name.split('#')[0].split('@')[0] in relactnames:
            rpcservices.log_start(name)
            if toldtowait:
                AGC.runActionGroup(name,times=times, rs=speedratio, sd=False, modu=modu)
            else:
                x=threading.Thread(target=AGC.runActionGroup,args=(name,times,speedratio,False,modu))
                x.start()#nice to return how long action would take
            rpcservices.log_stop()
            return json.dumps(rpcservices.log_get()[-1])#numbers in log (time?) too big. maybe rpc idea is not so great after all
        else:
            return ("error - action not exist: "+ name)


    server.register_function(rag, 'rag')

    # Run the server's main loop
    server.serve_forever()