import time
import Board

print('''
----------move camea a bit-
''')

for i in range(1,5):
    # 参数：参数1：舵机接口编号; 参数2：位置; 参数3：运行时间
    Board.setPWMServoPulse(2, 1500, 500)  # 2号舵机转到1500位置，用时500ms
    time.sleep(0.5)  # 延时时间和运行时间相同
    
    Board.setPWMServoPulse(2, 1800, 500)  #舵机的转动范围0-180度，对应的脉宽为500-2500,即参数2的范围为500-2500
    time.sleep(0.5)
    
    Board.setPWMServoPulse(2, 1500, 200)
    time.sleep(0.2)
    
    Board.setPWMServoPulse(2, 1800, 500)  
    Board.setPWMServoPulse(1, 1800, 500)
    time.sleep(0.5)
    
    Board.setPWMServoPulse(2, 1500, 500)  
    Board.setPWMServoPulse(1, 1500, 500)
    time.sleep(0.5)    
