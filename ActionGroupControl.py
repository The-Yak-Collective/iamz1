#!/usr/bin/env python3
# encoding: utf-8
#modified to also read csv files as rel-type (enhanced action group) files
#each row is a time followed by a series of settings (as strings!) per servo
#number (not zero) = absolute location
#+N or -N - relative movement + we keep track of values (they are windowed by Board)
#NOP  - do nothing
#L/UL - lock or unlock this servo

import os
import sys
import time
import threading
import sqlite3 as sql
from BusServoCmd import *
from Board import setBusServoPulse, stopBusServo
import csv

# PC software editor action call library

runningAction = False
stop_action = False
stop_action_group = False

def stopAction():
    global stop_action
    
    stop_action = True

def runActionGroup(actName, times=1):
    global stop_action
    global stop_action_group

    stop_action = False

    temp = times
    while True:
        if temp != 0:
            times -= 1
            if times < 0 or stop_action_group: # Out of the loop
                stop_action_group = False
                break
            runAction(actName)
        elif temp == 0:
            if stop_action_group: # Out of the loop
                stop_action_group = False
                break
            runAction(actName)

def runAction(actNum, lock_servos=''):
    '''
    Running action group, can not send stop signal
    :param actNum: action group name, character string stype
    :param times:  run times
    :return:
    '''
    global runningAction
    global stop_action
    global stop_action_group

    cur_state=[0]*18

    if actNum is None:
        return

    actNum = "/home/pi/SpiderPi/ActionGroups/" + actNum + ".d6a"
    relNum = "/home/pi/SpiderPi/ActionGroups/" + actNum + ".csv" #rather than in rels!
    if os.path.exists(actNum) is True:
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
                        if int(act[i+2]) < 0):
                            continue #attempt to make negative numbers into "NOP". maybe thsi was original intention of lock_servos
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
    elif os.path.exists(relNum) is True: #do the rel type action group file
        if runningAction is False:
            runningAction = True
            with open(relNum,newline='') as csvfile:
                readcsv=csv.reader(csvfile) #consider dictreader later
                for i in range(1,19):
                    cur_state[i]=int(Board.getBusServoPulse(i))#yes, slow. but we need it for relative movement. i guess we can run this only if we have an actual rel instruction and only for those entries. and maybe only first time they get called. TBD for now as this should work, even if slower
                for row in readcsv:
                    if stop_action:
                        stop_action_group = True
                        break
                    usetime=int(row[1])#row[0]=index of row, shouldbe
                    for i in range(2, len(row)): #we will use same general format as d6a files
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
                            Board.unLoadBusServo(i-1) #but then if it is moved passively, we actually do not know where it is and do not read the position because our reading is simply too slow!
                        elif entry=="L" or entry=="LOAD":
                            Board.LoadBusServo(i-1)
                    for j in range(int(usetime/50)):#left this in though i do not like it
                        if stop_action:
                            stop_action_group = True
                            break
                        time.sleep(0.05)
                    time.sleep(0.001 + usetime/1000.0 - 0.05*int(usetime/50))
                runningAction = False


    else:
        runningAction = False
        print("未能找到动作组文件")
