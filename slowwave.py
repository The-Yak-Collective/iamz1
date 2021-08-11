#!/usr/bin/python3
#slowwave
import Board
import time
t=3000
while True:
  Board.setBusServoPulse(1,200,t)
  time.sleep(t/2000.0)
  for i in range(1,19):
    x=Board.getBusServoPulse(i)
    print(x)
  time.sleep(t/2000.0)
  Board.setBusServoPulse(1,900,t)
  time.sleep(t/1000.0)
