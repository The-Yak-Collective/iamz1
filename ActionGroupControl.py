#!/usr/bin/env python3
# encoding: utf-8
#modified to also read csv files as rel-type (enhanced action group) files
#each row is a time followed by a series of settings (as strings!) per servo
#string format
#number (not zero) = absolute location
#+N or -N - relative movement + we keep track of values (they are windowed by Board)
#NOP  - do nothing
#L/UL - lock or unlock this servo
#actionname#number (or #N1#N2...), uses number as number of the leg to apply the file on. an alternative woudl be to have a different file format (with fewer items) when doing only one leg. but using leg as a filter seems easier to implement
#actionname@I - insist on action working as described
#actionname@F - just give feedback on plan vs actual
# @ comes after #

#CSV has priority over d6a


import os
import sys
import time
import threading
import sqlite3 as sql
from BusServoCmd import *
from Board import setBusServoPulse, getBusServoPulse, stopBusServo, unloadBusServo, loadBusServo
import csv
# onroverdb: sqlite3 file. for now, we will only write variables there and read modulation data from it
import json
from dotenv import load_dotenv, find_dotenv
import rpcservices

load_dotenv(find_dotenv())
ACTDIR=os.getenv('ACTDIR','/home/pi/SpiderPi/ActionGroups/')

# PC software editor action call library

runningAction = False
stop_action = False
stop_action_group = False
modulate = False #not implemented for now, needs modulate command in seq and also in rag (so it can get here). modulate file (should be) put into sqlite in seq
savedata=False
modulation_value = 1.0

def stopAction():
    global stop_action
    
    stop_action = True

def runActionGroup(actName, times=1, rs=1.0, modu = False, sd=True): #save data. who knows...
    global stop_action
    global stop_action_group
    global modulate
    global savedata

    stop_action = False
    modulate=modu
    savedata=sd

    temp = times
    while True:
        if temp != 0:
            times -= 1
            if times < 0 or stop_action_group: # Out of the loop
                stop_action_group = False
                break
            runAction(actName, rs=rs)
        elif temp == 0:
            if stop_action_group: # Out of the loop
                stop_action_group = False
                break
            return runAction(actName, rs=rs)
    return ("done actiongroup: "+actName)

def measure_state():
    return [0]+rpcservices.leg_pos()[1] # now using service. hopefully fasterru
    x=[0]*19
    for i in range(1,19):
        x[i]=int(getBusServoPulse(i))#yes, slow. but we need it for relative movement. i guess we can run this only if we have an actual rel instruction and only for those entries. and maybe only first time they get called. TBD for now as this should work, even if slower
    return x


def runAction(actNum, lock_servos='',rs=1.0):
    '''
    Running action group, can not send stop signal
    :param actNum: action group name, character string stype
    :param times:  run times
    :return:
    '''
    global runningAction
    global stop_action
    global stop_action_group
    global modulate
    global savedata
    
    starttime=int(time.time()*1000)
    feedback = False
    insist=False
    cur_state=[0]*19 #servos numbers 1 to 18
    filter=False
    filtercontents=[]

    if actNum is None:
        return
    temp=actNum.split('@')
    actNum=temp[0]
    if len(temp)>1:
        if temp[1][0]=='F':
            feedback=True
        if temp[1][0]=='I':
            insist=True
    #print(insist,feedback,temp)
    temp=actNum.split('#')
    actNum=temp[0]
    if len(temp)>1:
        filter=True
        for i in temp[1:]:
            firstservo=int(i)*3-2
            filtercontents.extend([firstservo,firstservo+1,firstservo+2])
    relNum = ACTDIR + actNum + ".csv" #rather than in rels! and do this first because action name is corrupted by processing
    actNum = ACTDIR + actNum + ".d6a"

    if os.path.exists(relNum) is True: #do the rel type action group file
        runningAction=False #need to delete this. anyway, it seems to intefere with recursion
        if runningAction is False:
            runningAction = True
            with open(relNum,newline='') as csvfile:
                readcsv=csv.reader(csvfile) #consider dictreader later. also check to see if first line is read as fields or not
                headers = next(readcsv, None) #yup, line 1 is read as data
                if modulate:
                    con1=sql.connect("onroverdb")
                    cur1=con1.cursor()
                for i in range(1,19):
                    cur_state=measure_state()
                for row in readcsv:
                    if stop_action:
                        stop_action_group = True
                        break
                    nowtime=int(time.time()*1000)
                    if modulate:
                        cur1.execute("select rs from modulation where time=?",(nowtime-nowtime%100,))
                        v=cur1.fetchone()
                        modulation_value=float(v[0]) if v else 1.0
                    else:
                        modulation_value=1.0
                    usetime=int(int(row[1])/(rs*modulation_value))#row[0]=index of row, shouldbe
                    for i in range(2, len(row)): #we will use same general format as d6a files
                        if filter and not (i-1 in filtercontents):
                            continue
                        entry=row[i]
                        if entry=="NOP":
                            continue
                        elif entry.isdigit():
                            theval=int(entry)
                            setBusServoPulse(i - 1, theval, usetime)
                            cur_state[i-1]=theval
                        elif entry[0]=="+":
                            theval=int(entry[1:])
                            setBusServoPulse(i - 1, cur_state[i-1]+theval, usetime)
                            cur_state[i-1]=cur_state[i-1]+theval
                            #consider first reading position rather than using local store. we will, once/if it is fast enough. similarly, we cannot actually assume that it reaches the current state as suggested. OTOH, if we do calculate rather than read, we allow relative movments to work properly even if cut off. so not clear what the best thing to do is
                        elif entry[0]=="-":
                            theval=int(entry[1:])
                            setBusServoPulse(i - 1, cur_state[i-1]-theval, usetime)
                            cur_state[i-1]=cur_state[i-1]-theval
                        elif entry=="UL" or entry=="UNLOAD":
                            unloadBusServo(i-1) #but then if it is moved passively, we actually do not know where it is and do not read the position because our reading is simply too slow!
                        elif entry=="L" or entry=="LOAD":
                            loadBusServo(i-1)
                    for j in range(int(usetime/50)):#left this in though i do not like it
                        if stop_action:
                            stop_action_group = True
                            break
                        time.sleep(0.05)
                    time.sleep(0.001 + usetime/1000.0 - 0.05*int(usetime/50))
                estimated_state=cur_state.copy()
                endtime=int(time.time()*1000)
                if insist:
                    cur_state=measure_state()
                    serror=[]
                    for x,y in zip(estimated_state[1:],cur_state[1:]): #do on 18 sized array
                        serror.append((int(x)-int(y))*(int(x)-int(y)))
                    lerror=[0,0,0,0,0,0]
                    for i,s in enumerate(serror):
                        lerror[int(i/3)]+=s
                    print (lerror,serror)
                    for i,l in enumerate(lerror):
                        if l>1000:#empirical number based on typical error in leaves being 1600 for all legs together. and then upadted based on actual stuff happeneing
                            print("error=",l,"leg=",i)
                            runAction("legfree1#"+str(i+1))
                            #runAction("legfree2#"+str(i+1))
                if feedback or savedata: #no difference for now
                    cur_state=measure_state()
                    print("we should be at:",estimated_state)
                    print("we are at:",cur_state)
                    toterror=0
                    for x,y in zip(estimated_state,cur_state):
                        toterror+=(int(x)-int(y))*(int(x)-int(y))
                    print("square of error is:",toterror)
                    #later define a threshold above which we report, etc.
                    #later define a way by which this feedback actually gets to user...
                if savedata:
                    con=sql.connect("onroverdb")
                    cur=con.cursor()
                    cur.execute("REPLACE INTO sharedvalues VALUES (?,?,?)",("cur_state",json.dumps(cur_state),endtime))
                    cur.execute("REPLACE INTO sharedvalues VALUES (?,?,?)",("estimated_state",json.dumps(estimated_state),endtime))
                    cur.execute("REPLACE INTO sharedvalues VALUES (?,?,?)",("toterror",json.dumps(toterror),endtime))
                runningAction = False
                if feedback:
                    with open('trackfeedback','a') as f:
                        print("we should be at:",*estimated_state, file=f)
                        print("we are at:",*cur_state, file=f)
                        print("total error:", toterror,file=f)
                        #f.write("testline")
                    return(estimated_state,cur_state, toterror)
    elif os.path.exists(actNum) is True:
        if runningAction is False:
            runningAction = True
            ag = sql.connect(actNum)
            cu = ag.cursor()
            cu.execute("select * from ActionGroup")
            while True:
                act = cu.fetchone()
                if stop_action:
                    stop_action_group = True
                    break
                if act is not None:
                    for i in range(0, len(act) - 2, 1):
                        if (int(act[i+2]) < 0):
                            continue #attempt to make negative numbers into "NOP". maybe this was original intention of lock_servos
                        elif str(i + 1) in lock_servos:
                            setBusServoPulse(i + 1, lock_servos[str(i + 1)], act[1])
                        else:
                            setBusServoPulse(i + 1, act[2 + i], act[1])
                    for j in range(int(act[1]/50)):
                        if stop_action:
                            stop_action_group = True
                            break
                        time.sleep(0.05)
                    time.sleep(0.001 + act[1]/1000.0 - 0.05*int(act[1]/50))
                else:   # run complete exit
                    break
            runningAction = False
            
            cu.close()
            ag.close()

    else:
        runningAction = False
        print("未能找到动作组文件", actNum,relNum)
