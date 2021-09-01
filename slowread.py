#!/usr/bin/python3
#slowwave - moved read to "slowread.py"
import Board
import time
import datetime
t=3000
while True:
    print("start:",datetime.datetime.now())
    for i in range(1,19):
        x=Board.getBusServoPulse(i)
        print(x,datetime.datetime.now())
    time.sleep(0.1)

