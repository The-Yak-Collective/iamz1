import servo_util
import xmlrpc.client
import json
PORTFORLOGGING=9501 # later we will make this an env variable. for now, use 9500-9550
PORTFORLEGS=9502 #position of each servo

logging = xmlrpc.client.ServerProxy('http://localhost:'+str(PORTFORLOGGING))

def log_start(command):
    logging.logstart(command)
def log_stop():
    logging.logstop()
def log_get():
    g=logging.logget()
    return json.loads(g)
    
legs = xmlrpc.client.ServerProxy('http://localhost:'+str(PORTFORLEGS))

def leg_pos():
    return legs.legpos()
