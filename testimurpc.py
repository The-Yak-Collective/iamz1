import time
import rpcservices

while True:
    t=time.time()
    print("imu:",rpcservices.getimudata())
    print("leg:",rpcservices.leg_pos())
    t1=time.time()
    tts=0.1-(t1-t)
    print(t, t1, tts)
    if tts>0:
        time.sleep(tts)