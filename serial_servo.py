#!/usr/bin/python3
# coding=utf8

import time
import serial

serialHandle = serial.Serial("/dev/ttyAMA0", 9600)  #初始化串口， 波特率为9600

CMD_SERVO_MOVE          = 0x03   #控制舵机指令
CMD_ACTION_GROUP_RUN    = 0x06   #运行动作组指令
CMD_ACTION_GROUP_STOP   = 0x07   #停止动作组运行指令
CMD_ACTION_GROUP_SPEED  = 0x0B   #设置动作组运行速度指令

# 运行动作组
def runActionGroup(number, time):
    '''
    number: 动作组编号
    time: 运行次数
    '''
    buf = bytearray(b'\x55\x55')
    cmd = CMD_ACTION_GROUP_RUN
    
    try:
        data_len = 5   # 数据长度
        buf.extend([data_len, cmd, number])
        buf.extend([(0xff & time), (0xff & (time >> 8))])  #分低8位 高8位
        serialHandle.write(buf) #发送
        
    except Exception as e:
        print(e)

# 停止运行动作组
def stopActionGroup():
    
    buf = bytearray(b'\x55\x55')
    cmd = CMD_ACTION_GROUP_STOP
    
    try:
        data_len = 2   # 数据长度
        buf.extend([data_len, cmd ])
        serialHandle.write(buf) #发送
        
    except Exception as e:
        print(e)

# 设置运行动作组速度
def setActionGroupSpeed(number, speed):
    '''
    number: 动作组编号
    speed: 运行速度
    '''
    buf = bytearray(b'\x55\x55')
    cmd = CMD_ACTION_GROUP_SPEED
    
    try:
        data_len = 5   # 数据长度
        buf.extend([data_len, cmd, number])
        buf.extend([(0xff & speed), (0xff & (speed >> 8))])  #分低8位 高8位
        serialHandle.write(buf) #发送
        
    except Exception as e:
        print(e)

# 驱动单个舵机
def moveServo(id, pulse, time):
    '''
    id: 舵机编号
    pulse: 脉冲(PWM舵机:500~2500, 串口舵机:500~2500)
    time: 运行时间
    '''
    buf = bytearray(b'\x55\x55')
    cmd = CMD_SERVO_MOVE
    
    try:
        data_len = 8   # 数据长度
        num = 1
        
        buf.extend([data_len, cmd, num])
        buf.extend([(0xff & time), (0xff & (time >> 8))])  #分低8位 高8位 
        buf.append(id)
        buf.extend([(0xff & pulse), (0xff & (pulse >> 8))])  #分低8位 高8位 
        
        serialHandle.write(buf) #发送
        
    except Exception as e:
        print(e)

# 驱动多个舵机
def moveServos(*args):
    '''
    args: 参数(运行时间, 舵机个数, id1, pulse1, id2, pulse2, id3, pulse3, ...)
    idx: 舵机编号
    pulsex: 脉冲(PWM舵机:500~2500, 串口舵机:500~2500)
    '''
    buf = bytearray(b'\x55\x55')
    cmd = CMD_SERVO_MOVE
    arglen = len(args)
    
    try:
        use_times = args[0]
        servos_num = args[1]  
        servos = args[2:arglen:2]
        pulses = args[3:arglen:2]  
        
        data_len = servos_num * 3 + 5   # 数据长度
        buf.extend([data_len, cmd, servos_num])
        buf.extend([(0xff & use_times), (0xff & (use_times >> 8))])  #分低8位 高8位
        data = zip(servos, pulses)
        for (i, p) in data:
            buf.append(i)
            buf.extend([(0xff & p), (0xff & (p >> 8))])  #分低8位 高8位
            
        serialHandle.write(buf) #发送
        
    except Exception as e:
        print(e)


if __name__ == '__main__':
    try:
        setActionGroupSpeed(8, 200)
        runActionGroup(8,2)
        time.sleep(6)
        stopActionGroup()
        time.sleep(0.1)
        setActionGroupSpeed(8, 50)
        runActionGroup(8,1)
        time.sleep(3)
    #     
        moveServo(1,500,1500)
        time.sleep(1.5)
        moveServo(1,2500,1500)
        moveServos(1500, 5, 1,500, 2,500, 3,500, 4,500, 5,500)
        time.sleep(1.5)
        moveServos(1500, 5, 1,2500, 2,2500, 3,2500, 4,2500, 5,2500)
        print("ok")

    except Exception as e:
        print(e)

    
    