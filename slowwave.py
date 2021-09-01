#!/usr/bin/python3
#slowwave - moved read to "slowread.py"
import Board
import time
import datetime
tr=0
t=3000
while True:
  print("move command ",tr, datetime.datetime.now()) #lets see if it simply delays while waiting or gets lost
  tr=tr+1
  Board.setBusServoPulse(1,200,t)
  time.sleep(t/2000.0)
  #for i in range(1,19):
  #  x=Board.getBusServoPulse(i)
  #  print(x)
  time.sleep(t/2000.0)
  Board.setBusServoPulse(1,900,t)
  time.sleep(t/1000.0)
