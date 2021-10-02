#run as a iamz1 command
#like this: $WWG seq filename (default filename="seqfile")
#filenames can be uploaded or prepared locally (2nd option for 1st phase)
#format:
    #lines.
    #each line is:
        #wait - wait for each command to finish (up to 10 seconds) before doing next (implemented by rag)
        #nowait - send commands to bot as they are read. each line is run as a sperate python script, if relevent
        #pause S - pause X milliseconds
        #push X - state of leg #X pushed to stack (one stack per leg). stack local to execution
        #pop X S - pop the state of leg X, do it in time S milliseconds
        #rag action_group N SR (all parameters needed) - do action group N times, at speed ratio (float) SR
        #rel action_command N SR - do an action command (like an action group but allowing both relative and absolute position movement and also allowing "NOP" (and unlock? or lock) in an action group line), at speed ratio SR. action commands stored in a separate directory and maybe they have a plain text format. or maybe csv, but strings. what is advantage of sqlite3 files? if we want backwards compatibility, we need to maybe add a table of "modifications". but that is not human readable... so using CSV instead, but in same directory as action groups. work in progress...
#TBD - how to modulate the whole file using music/rhythm/etc

#other files to recode: rel.py, rag.py


import os
import time
import subprocess
import Board

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
WHEREIRUNDIR=os.getenv('WHEREIRUNDIR',default="/media/pi/z1-drive/maier/iamz1/") 

print('''
run a sequence of commands from a file:
usage: python3 seq.py [file_name] [times]
''')


args=sys.argv
towait=True
stack=[[],[],[],[],[],[]]
if(len(args)<2): 
    seqfile="seqfile"
else:
    seqfile=args[1]

if(len(args)<3): 
    times=1
else:
    times=int(args[2])

with open(seqfile) as thefile:
    lines=thefile.readlines()

for rep in range(times):
    for line in lines:
        words=line.split()
        lencom=len(words)
        if words[0]=="wait" and lencom==1:
            towait=True
        elif words[0]=="nowait" and lencom==1:
            towait=False
        elif words[0]=="pause" and lencom==1:
            time.sleep(float(words[1])/1000.0)
        elif words[0]=="push"and lencom==2:
            #read angles of three servos on a leg, into angles
            numeric=words[1]
            angles=(Board.getBusServoPulse(numeric*3-2),Board.getBusServoPulse(numeric*3-1),Board.getBusServoPulse(numeric*3))
            stack[numeric].append(angles)
        elif words[0]=="pop" and lencom==3:
            numeric=words[1]
            usetime=int(words[2])
            if len(stack[numeric])<1:
                print("empty stack!", words[1])
            else:
                angles=stack[numeric].pop()
                for idx,a in enumerate(angles):
                    Board.setBusServoPulse((numeric-1)*3+idx+1, int(a), usetime):
        elif (words[0]=="rag" or words[0]=="rel") and lencom==4:
            name=words[1]
            args=words[2]
            speedratio=float(words[3]) #not actually implemented yet, would be by a change in actiongroupcontrol.py
            out = subprocess.Popen(['/usr/bin/python3', words[0]+'.py', name]+list(args)+list(str(speedratio)),
               cwd=WHEREIRUNDIR,
               stdout=subprocess.PIPE, 
               stderr=subprocess.STDOUT)
            if towait:
                try:
                    stdout,stderr = out.communicate(timeout=10)#assume no rag or rel is more than 10 seconds. otherwise do not wait more
                except subprocess.TimeoutExpired:
                    pass
        else:
            print("command {} not supported. maybe wrong number of parameters or a mispelling".format(line))





