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
        #rag action_command N SR - (but now with rel option - if no .d6a file found) do an action command (like an action group but allowing both relative and absolute position movement and also allowing "NOP" (and unlock? or lock) in an action group line), at speed ratio SR. action commands stored in a separate directory and maybe they have a plain text format. or maybe csv, but strings. what is advantage of sqlite3 files? if we want backwards compatibility, we need to maybe add a table of "modifications". but that is not human readable... so using CSV instead, but in same directory as action groups. work in progress...
        #leg X action_group_name N SR - apply action group file only to leg X. underlying mechanism supports having multiple legs affected
        #seq filename times modulate savedata: recursively run seq on a new file. if you change the modulation. it ruins it for parent. not  tested yet
        #modulate on/off/filename [repeats] starts modulatin, stops modulation or loads file (repeats times) into sqlite. note modulation timing is synchronized to the modulate command, not the on command, so rag, etc. can use absolute timing
        #printstat - show estimate and actual values


#TBD command: on xxx yyy - executes command yyy is condition xxx happens. needs to be defined, but basically leg acting all funny and stuff. better - make xxx a python script that returns true/false or maybe simply a python function. yyy is one of the standard commands in file





import sys
import os
import time
import subprocess
import Board
import sqlite3 as sql

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
WHEREIRUNDIR=os.getenv('WHEREIRUNDIR',default="/media/pi/z1-drive/maier/iamz1/") 

print('''
run a sequence of commands from a file:
usage: python3 seq.py [file_name] [times] [modulate (True/False)] [[savedata (True/False)]
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

if(len(args)<4): 
    modulate=False
else:
    modulate= not (args[3] in ['false','False'])

if(len(args)<5): 
    savedata=False
else:
    savedata= not (args[4] in ['false','False'])

with open(seqfile) as thefile:
    lines=thefile.readlines()

for rep in range(times):
    for line in lines:
        line.strip()
        if line[0]=="#":
            continue
        words=line.split()
        lencom=len(words)
        if lencom==0:
            continue
        if words[0]=="wait" and lencom==1:
            towait=True
        elif words[0]=="nowait" and lencom==1:
            towait=False
        elif words[0]=="printstat" and lencom==1:
            con=sql.connect("onroverdb")
            cur=con.cursor()
            cur.execute("select * from sharedvalues where name=?",("cur_state",))
            row=cur.fetchone()
            if row:
                time=int(row[2])
                cur_state=json.loads(row[1])

            cur.execute("select * from sharedvalues where name=?",("estimated_state",))
            row=cur.fetchone()
            if row:
                estimated_state=json.loads(row[1])
            
            cur.execute("select * from sharedvalues where name=?",("toterror",))
            row=cur.fetchone()
            if row:
                toterror=json.loads(row[1])
            print("found in sqlite:",cur_state,estimated_state,toterror)
        elif words[0]=="pause" and lencom==2:
            time.sleep(float(words[1])/1000.0)
        elif words[0]=="modulate":
            if words[1]=='on'and lencom==2:
                modulate=True
            elif words[1]=='off'and lencom==2:
                modulate=False
            elif lencom>1:
                mfilename=words[1]
                with open(mfilename) as f:
                    rhythm=f.readlines()
                starttime=int(time.time()*1000)
                t=0
                con=sql.connect("onroverdb")
                cur=con.cursor()
                cur=con.execute('delete * from modulation')
                repeats=1
                if lencom==3:
                    repeats=int(words[2])
                for count in range(repeats)
                    for r in rhythm:
                        cur.execute("insert INTO modulation VALUES (?,?,?)",(starttime+100*t,float(r),""))
                        t=t+1 #one line per 100ms

        elif words[0]=="push"and lencom==2:
            #read angles of three servos on a leg, into angles
            numeric=int(words[1])
            angles=(Board.getBusServoPulse(numeric*3-2),Board.getBusServoPulse(numeric*3-1),Board.getBusServoPulse(numeric*3))
            stack[numeric].append(angles)
        elif words[0]=="pop" and lencom==3:
            numeric=int(words[1])
            usetime=int(words[2])
            if len(stack[numeric])<1:
                print("empty stack!", words[1])
            else:
                angles=stack[numeric].pop()
                for idx,a in enumerate(angles):
                    Board.setBusServoPulse((numeric-1)*3+idx+1, int(a), usetime)
        elif (words[0]=="rag" and lencom==4) or (words[0]=='leg' and lencom==5):
            if lencom==4: #rag command
                name=words[1]
                args=words[2]
                speedratio=float(words[3]) #not actually implemented yet, would be by a change in actiongroupcontrol.py. actally, maybe it is now
                
            elif lencom==5: #leg command - can go really wild and define leg 0 as all the legs. note if words[1] is 1#2#3, all three get sent on
                name=words[2]+'#'+words[1]
                args=words[3]
                speedratio=float(words[4]) #not actually implemented yet, would be by a change in actiongroupcontrol.py. maybe it is actually.

            out = subprocess.Popen(['/usr/bin/python3', 'rag.py', name]+list(args)+list(str(speedratio))+list(str(modulate))+list(str(savedata)),
               cwd=WHEREIRUNDIR,
               stdout=subprocess.PIPE, 
               stderr=subprocess.STDOUT)
            if towait: #if not waiting, cannot do an "on error" command
                try:
                    stdout,stderr = out.communicate(timeout=10)#assume no rag or rel is more than 10 seconds. otherwise do not wait more
                except subprocess.TimeoutExpired:
                    pass
        elif (words[0]=="seq" and lencom==5):
            name=words[1]
            out = subprocess.Popen(['/usr/bin/python3', 'seq.py', name]+words[2:]),
               cwd=WHEREIRUNDIR,
               stdout=subprocess.PIPE, 
               stderr=subprocess.STDOUT)
            if towait: #if not waiting, cannot do an "on error" command
                try:
                    stdout,stderr = out.communicate(timeout=30)#assume no seq is more than 30 seconds
                except subprocess.TimeoutExpired:
                    pass

        else:
            print("command {} not supported. maybe wrong number of parameters or a mispelling".format(line))





