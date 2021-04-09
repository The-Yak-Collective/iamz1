import time
import Board
from testunload import *

print('''
**********************************************************
*****功能:幻尔科技SpiderPi扩展板，串口舵机读取状态例程******
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
以下指令均需在LX终端使用，LX终端可通过ctrl+alt+t打开，或点
击上栏的黑色LX终端图标。
----------------------------------------------------------
Usage:
    sudo python3 BusServoReadStatus.py
----------------------------------------------------------
Version: --V1.1  2020/11/13
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！
----------------------------------------------------------
''')

def getBusServoStatus(ser):
    Pulse = Board.getBusServoPulse(ser)  # 获取9号舵机的位置信息
    Temp = Board.getBusServoTemp(ser)  # 获取9号舵机的温度信息
    Vin = Board.getBusServoVin(ser)  # 获取9号舵机的电压信息
    return (Pulse,Temp,Vin)
#    time.sleep(0.5)  # 延时方便查看

while True:   
#    Board.setBusServoPulse(9, 500, 1000) # 9号舵机转到500位置用时1000ms
    time.sleep(1)
    for x in range(1,18):
        y=getBusServoStatus(x)
        Pulse,Temp,Vin=y
        serial_servo_read_cmd(id=x, r_cmd=LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
        ret=serial_servo_get_rmsg(LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
        print('ret=',ret)
        print('ser: {} Pulse: {}\tTemp:  {}℃\tVin:   {}mV\n'.format(x, Pulse, Temp, Vin)) # 打印状态信息
#    Board.setBusServoPulse(9, 300, 1000)
#    time.sleep(1)
#    getBusServoStatus()
