#convert d6a files to csv files so that system can use them
import os
import sys
import time

import sqlite3 as sql

import csv

header=["Index","Time","Servo1","Servo2","Servo3","Servo4","Servo5","Servo6","Servo7","Servo8","Servo9","Servo10","Servo11","Servo12","Servo13","Servo14","Servo15","Servo16","Servo17","Servo18"]
for file in sys.argv[1:]:
    ag = sql.connect(file)
    cu = ag.cursor()
    cu.execute("select * from ActionGroup")
    with open(file[:-4]+'.csv',"w") as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(header)
        while True:
            act = cu.fetchone()
            if not act:
                break
            writer.writerow(act)
            readcsv=csv.reader(csvfile) #consider 
